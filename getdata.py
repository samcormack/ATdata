import os
import sys
import django

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'sitemain/')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from google.transit import gtfs_realtime_pb2
from apipull.models import RTentry,Route,Stop,CallRecord
from django.utils import timezone
from django.conf import settings
from datetime import datetime
import requests
import json

class DataGrabber():
	def __init__(self):
		self.callrecord = CallRecord()
		self.feed = gtfs_realtime_pb2.FeedMessage()
		self.routesfeed = {}
		self.stopsfeed = {}


	def get_realtime_GTFS(self):
	## Get GTFS-realtime data from AT API
		headerspb = {'Accept':'application/x-protobuf','Ocp-Apim-Subscription-Key': settings.AT_API_KEY}
		url = "https://api.at.govt.nz/v2/public/realtime/tripupdates"
		try:
			response = requests.get(url,headers=headerspb)
			response.raise_for_status()
		except ConnectionError:
			self.callrecord.connected=False
		except HTTPError:
			self.callrecord.http_status = response.status_code
		else:
			self.callrecord.connected = True
			self.callrecord.http_status = response.status_code
			self.feed.ParseFromString(response.content)
		self.callrecord.save()

	def get_static_GTFS(self):
		## Get static GTFS from AT api
		headerspb = {'Ocp-Apim-Subscription-Key': settings.AT_API_KEY}
		# Routes
		url = "https://api.at.govt.nz/v2/gtfs/routes"
		response = requests.get(url,headers=headerspb)
		self.routesfeed = response.json()
		# stops
		url = "https://api.at.govt.nz/v2/gtfs/stops"
		response = requests.get(url,headers=headerspb)
		self.stopsfeed = response.json()

	def routes_from_json(self):
		routes = self.routesfeed['response']
		for rr in routes:
			if Route.objects.filter(route_id=rr['route_id']):
				continue
			else:
				rmod = Route()
				rmod.route_id = rr['route_id']
				rmod.agency_id = rr['agency_id']
				rmod.route_short_name = rr['route_short_name']
				rmod.route_long_name = rr['route_long_name']
				rmod.route_type = rr['route_type']
				rmod.save()

	def stops_from_json(self):
		stops = self.stopsfeed['response']
		for ss in stops:
			if Stop.objects.filter(stop_id=ss['stop_id']):
				continue
			else:
				smod = Stop()
				smod.stop_id = ss['stop_id']
				smod.stop_lat = ss['stop_lat']
				smod.stop_lon = ss['stop_lon']
				smod.location_type = ss['location_type']
				smod.stop_code = ss['stop_code']
				smod.stop_name = ss['stop_name']
				smod.save()

	def RTentries_from_pbuf(self):
		## Extract data from structure
		for entity in self.feed.entity:
			entry = RTentry()
			entry.call = self.callrecord
			if entity.HasField('trip_update'):
				entry.id_no = entity.id
				tu = entity.trip_update
				entry.trip_id = tu.trip.trip_id
				entry.route_id = Route.objects.get(pk=tu.trip.route_id)
				stu = tu.stop_time_update[0]
				entry.stop_seq = stu.stop_sequence
				if stu.HasField('departure'):
					entry.stop_type = 'departure'
					entry.delay = stu.departure.delay
					entry.time = stu.departure.time
				elif stu.HasField('arrival'):
					entry.stop_type = 'arrival'
					entry.delay = stu.arrival.delay
					entry.time = stu.arrival.time
				else:
					entry.stop_type = 'none'
					# entry.delay = np.nan
					# entry.time = np.nan
				entry.time = datetime.fromtimestamp(entry.time,tz=timezone.get_current_timezone())
				entry.stop_id = Stop.objects.get(pk=stu.stop_id)
				entry.vehicle_id = tu.vehicle.id
				if entry.delay >2**16:
					entry.delay = entry.delay - (2**32-1) # Fix signed int conversion

				# Static info

				entry.save()

if __name__ == "__main__":
	datagrabber = DataGrabber()
	datagrabber.get_static_GTFS()
	datagrabber.routes_from_json()
	datagrabber.stops_from_json()
	datagrabber.get_realtime_GTFS()
	datagrabber.RTentries_from_pbuf()

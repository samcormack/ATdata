from django.shortcuts import render
from .models import CallRecord

def call_log(request):
    call_list = CallRecord.objects.order_by('-timestamp')[:30]
    return render(request,'apipull/call_log.html',{'call_list': call_list})

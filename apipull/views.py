from django.shortcuts import render

def call_log(request):
    return render(request,'api_pull/call_log.html',{})

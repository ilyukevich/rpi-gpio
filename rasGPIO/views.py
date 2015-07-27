# -*- coding: utf-8 -*-
#тест верстки логика во views1!!!
from django.shortcuts import render
import time, os
from uptime import uptime
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from forms import *
from models import *

def cpu_temp():
    res = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    res = res.replace('\n', '')
    return float(res)/1000

def cpu_load():
    res = os.popen('uptime').readline()
    res = res.replace('\n', '')
    pos = res.index('age:')
    return "%s " % res[pos+5:pos+9]

def dth11():
    data = os.popen('./dht11').readline().replace('\n','').split(',')
    return data

def timeup():
    time=int(uptime())
    mins=time/60
    hours=mins/60
    days=hours/24
    return "%d д. %d ч. %d м." % (days%30, hours%24, mins%60) 

LAST_TMPR, LAST_HMDT = 0, 0

def controlls(request):
    return render(request, "controlls.html", {  'temper':cpu_temp(),
                                        	'load':cpu_load,
                                        	'timeup': timeup(),
						}) 
	
def login(request):
    if request.user.is_authenticated():
	return HttpResponseRedirect('/')
    if request.POST:
	username=request.POST['username']
	password=request.POST['password']
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
           auth.login(request, user)
           return HttpResponseRedirect(request.GET.get('next', '/'))
        else:
	   return render(request, 'login.html', {
                'error': 1,
		'username': username,
            	})
    return render(request, "login.html",{})

@login_required
def reboot(request):
    responce={}
    if request.POST:
	a=1
	#do ajax reboot
	if request.user.controlluser.privig <= 1:
	   status=1
	   msg=u'Внимание!\nRaspberry PI сейчас перезагрузится!'
	else:
	   msg=u'Недостаточно прав! Обратитесь к админимтратору.'
	   status=0
	responce['msg']=msg
	responce['status']=status
    	jsondata=json.dumps(responce)
    	return HttpResponse(jsondata, content_type='application/json')

@login_required
def logout_v(request, page='/'):
    auth.logout(request)
    return HttpResponseRedirect(page)

@login_required
def switch(request):
    response={}
    if request.POST and 'is_activate' in request.POST and 'id' in request.POST:
	if user.user.controlluser.privig < 3:
	   activate=int(request.POST.get('is_activate', 0))
	   num=int(request.POST.get('id', 1))
	   pio.output(RELAY[num-1], not bool(activate))
    	   response['status']=0 # ok, 1 no rules, 2 not auth
	   response['id']=num
	   response['prev']=activate
        else:
	   response['status']=1 
	   response['msg']=u'У вас недостаточно прав'
    else:
	response['status']=2
	response['msg']=u'Необходимо авторизоваться'
    jsondata=json.dumps(response)
    return HttpResponse(jsondata, content_type='application/json')
    


# -*- coding: utf-8 -*-
from django.shortcuts import render
import time, os

# pip install uptime
from uptime import uptime
from django.http import HttpResponse
import RPi.GPIO as gpio
import json
import logging
import tm1638

RELAY=[5, 6, 13, 19, 26, 16, 20, 21]

display=0

def sw(mask):
    display.set_text('deb')
    if mask&(1<<0):
	display.set_text('btn1')
    if mask&(1<<1):
	display.set_text('btn2')

def init_gpio():
   DIO = 17
   CLK = 27
   STB = 22
   global display
   display = tm1638.TM1638(DIO, CLK, STB)
   pio=display.enable(0)
   display.sw_callback=sw
   for r in RELAY:
     pio.setup(r, gpio.OUT)
     pio.output(r, 1)
   return pio

pio=init_gpio()

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
    states, i={}, 1
    dht=dth11()
    global LAST_TMPR, LAST_HMDT
    if len(dht)==2:
	tmpr, LAST_TMPR=dht[1], dht[1]
        hmdt, LAST_HMDT=dht[0], dht[0]
    else:
	tmpr, hmdt=LAST_TMPR, LAST_HMDT
    for r in RELAY:
	s=pio.input(r)
	states[i]=s
	i+=1  
    return render(request, "controlls.html", {  'temper':cpu_temp(),
                                        	'load':cpu_load,
                                        	'timeup': timeup(),
						'states':states,
                                        	'temperature':tmpr,
						'humidity':hmdt}) 
	
def login(request):
    return render(request, "login.html",{})

def switch(request):
    res='fail'
    if request.POST and 'is_activate' in request.POST and 'id' in request.POST:
	activate=int(request.POST.get('is_activate', 0))
	num=int(request.POST.get('id', 1))
	pio.output(RELAY[num-1], not bool(activate))
	res='ok'
    response = {
         'id': num,
         'res':res,
	 'prev':activate
    }
    jsondata=json.dumps(response)
    return HttpResponse(jsondata, content_type='application/json')
    


from django.conf.urls import include, url
from django.contrib import admin
from rasGPIO.views import *


urlpatterns = [
    # Examples:
    # url(r'^$', 'raspberryGPIO.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'rasGPIO.views.controlls', name='controlls'),
    url(r'^login$', 'rasGPIO.views.login', name='login'),
    url(r'^switch$', 'rasGPIO.views.switch', name='switch'),
    url(r'^reboot$', 'rasGPIO.views.reboot', name='reboot'),
    url(r'^loguot$', 'rasGPIO.views.logout_v', name='logout_v'),

]

from django.db import models
from django.contrib.auth.models import User
import datetime


class ControllUser(models.Model):
    """
    info
    #0 самые высокие + добавлять пользователей
	#1 + может перзагружать
	#2 + может менять состояние реле
	#3 + может смотреть всю информацию
	#4 может смотреть время работы
	"""

    registered = models.DateTimeField(default=datetime.datetime.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    privig = models.IntegerField(default=4)


    def __unicode__(self):
        return str(self.user.username).join(' ').join(str(self.privig))


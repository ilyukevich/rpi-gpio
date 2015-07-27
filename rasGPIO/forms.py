# -*- coding: utf-8 -*- 
from django import forms

class TM1638Form(forms.Form):
    title=forms.CharField(label=u'TM1638', max_length=100, 
				widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':u'Текст для tm1638'}))


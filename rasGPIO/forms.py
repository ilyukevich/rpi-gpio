from django import forms


class TM1638Form(forms.Form):
	"""info"""

	tm1638 = forms.CharField(label=u'TM1638', max_length=100,
							 widget=forms.TextInput(attrs={'placeholder':u'Текст для tm1638'}))


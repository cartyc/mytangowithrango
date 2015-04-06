from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, userProfile

class CategoryForms(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enteter the category name")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	# Meta class to provide information on the form
	class Meta:

		model = Category
		fields = ('name',)

class PageForms(forms.ModelForm):

	title = forms.CharField(max_length=128, help_text="Please enter the title of the page")
	url = forms.URLField(max_length=200, help_text="PLease enter the url of the page")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:

		model = Page

		exclude = ('Category',)


	def clean(self):

		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url

		return cleaned_data

class UserForms(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:

		model = User
		fields = ('username', 'email', 'password')


class UserProfileForms(forms.ModelForm):

	class Meta:

		model = userProfile
		fields = ('website', 'picture')
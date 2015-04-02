from django import forms
from rango.models import Page, Category

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
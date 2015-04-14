import json
import urllib, urllib2

#Bing API Key

BING_API_KEY = "deHx/9yPwgMh5rdnW4WQXjwWnD5vrQtFlYJfNA9xF+k"

def run_query(search_terms):

	root_url = 'https://api.datamarket.azure.com/Bing/Search/'
	source = "web"

	# Results Return
	results_per_page = 10
	offset = 0

	#Put quotes around the query
	query ="'{0}'".format(search_terms)
	query = urllib.quote(query)

	#Format backhalf of Url and set jSON formatting
	search_url = "{0}{1}?$format=json$top={2}&$skip={3}&"
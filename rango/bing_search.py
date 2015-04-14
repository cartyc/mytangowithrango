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
	search_url = "{0}{1}?$format=json$top={2}&$skip={3}&$Query={4}".format(
			root_url,
			source,
			results_per_page,
			offset,
			query
		)

	#User name must be blank. Don't forget to enter your API Key
	username = ''

	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, search_url, username, BING_API_KEY)

	result = []

	try:
		#Prepare API Communication
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.builder_opener(handler)

		urllib2.install_opener(opener)

		#connect to the server
		response = urllib2.urlopen(search_url).read()

		json_response = json.loads(response)

		#Loop through each page returned and populate results
		for result in json_response['d']['results']:
			results.append({
				'title': result['title'],
				'link' : result['Url'],
				'summary' : result['Description']
				})
	except urllib2.URlError, e:
		print "Error connecting to the bing API"

	#return the results
	return results

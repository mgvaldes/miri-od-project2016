import urllib
import httplib2

repository = 'foursquare_10'
graph      = 'http://restaurants.recommender.es/foursquare/'
filename   = 'foursquare.rdf'
# filename   = 'foursquare/restaurants_1.rdf'

print("Loading %s into %s in Sesame" % (filename, graph))
params = { 'context': '<' + graph + '>' }
endpoint = "http://localhost:8080/openrdf-sesame/repositories/%s/statements?%s" % (repository, urllib.parse.urlencode(params))
data = open(filename, 'r').read()
(response, content) = httplib2.Http().request(endpoint, 'PUT', body=data.encode('utf8'), headers={ 'content-type': 'application/rdf+xml' })
print("Response %s" % response.status)
print(content)
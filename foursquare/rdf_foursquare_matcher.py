import rdflib
import pyfoursquare as foursquare
import urllib
from difflib import SequenceMatcher
import operator

def similar(a, b):
    return SequenceMatcher(None, a.encode('utf8'), b.encode('utf8')).ratio()

g = rdflib.Graph()

g.parse("restaurants_20.rdf")

qres = g.query(
    """SELECT DISTINCT ?restname ?lat ?lon ?address
       WHERE {
          ?rest v:fn ?restname .
          ?rest v:geo ?geoloc .
          ?geoloc v:latitude ?lat .
          ?geoloc v:longitude ?lon .
          ?rest v:adr ?restaddr .
          ?restaddr v:street-address ?address.
       }""")

client_id = "OCUL4KUN0I1JLF4HANT2HONTAK2ORB1FQOE3O5MGIFNBY25G"
client_secret = "25X3X2IRD01M4UWR4DPA1NC4DUUUOJ3NCDMBM1QT5SIKSLKB"
callback = 'http://localhost:8080/'

auth = foursquare.OAuthHandler(client_id, client_secret, callback)

auth.set_access_token('DUXWBHZWHD2QHDJZKV15VHDK3FT2MWCNDYT42XZUTI5XRKCY')

#Now let's create an API
api = foursquare.API(auth)

# venues/search?ll=41.382,2.171&intent=browse&radius=5000&categoryId=4d4b7105d754a06374d81259&query=Bar%20Pinocho

for row in qres:
    aux_loc1 = row[1].split('.')
    aux_loc2 = row[2].split('.')
    # print '////////////////////////////////////////// RDF Restaurant: '
    # print row[0] + ' ' + aux_loc1[0] + '.' + aux_loc1[1][:3] + ' ' + aux_loc2[0] + '.' + aux_loc2[1][:3]
    rest_name_not_encoded = row[0].split('*')[0]
    rest_name = rest_name_not_encoded.encode('utf8')
    location = aux_loc1[0] + '.' + aux_loc1[1][:3] + ',' + aux_loc2[0] + '.' + aux_loc2[1][:3]
    # Now you can access the Foursquare API!
    results = api.venues_search(query=urllib.quote_plus(rest_name), ll=location, intent='browse', radius=5000,
                               categoryId='4d4b7105d754a06374d81259', limit=5)

    # print len(results)

    i = 0
    similarities = {}

    # print '-------- FOURSQUARE Results: '
    for result in results:
        if hasattr(result.location, 'address'):
            # print(result.name + ' ' + result.location.address)
            similarities[i] = similar(rest_name_not_encoded, result.name) * similar(row[3], result.location.address)

        i += 1

    if not similarities:
        print '-------- NO MATCH!!!'
        # print row[0] + ' ' + aux_loc1[0] + '.' + aux_loc1[1][:3] + ' ' + aux_loc2[0] + '.' + aux_loc2[1][:3] + ' ' + row[3]
    else:
        max_sim = max(similarities.iteritems(), key=operator.itemgetter(1))
        max_similarity_result = results[max_sim[0]]

        if max_sim[1] > 0.3:
            print '************************************************************ FINAL MATCH WITH SIM: ' + str(max_sim[1])
            print row[0] + ' ' + aux_loc1[0] + '.' + aux_loc1[1][:3] + ' ' + aux_loc2[0] + '.' + aux_loc2[1][:3] + ' ' + row[3]

            aux_loc3 = str(max_similarity_result.location.lat).split('.')
            aux_loc4 = str(max_similarity_result.location.lng).split('.')
            print max_similarity_result.name + ' ' + aux_loc3[0] + '.' + aux_loc3[1][:3] + ' ' + aux_loc4[0] + '.' + aux_loc4[1][:3] + ' ' + max_similarity_result.location.address
        else:
            print '-------- NO MATCH!!!'
            # print row[0] + ' ' + aux_loc1[0] + '.' + aux_loc1[1][:3] + ' ' + aux_loc2[0] + '.' + aux_loc2[1][:3] + ' ' + row[3]
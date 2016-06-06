import urllib
import httplib2
import xml.etree.ElementTree as ET
import unicodedata
from nltk.corpus import stopwords
import re
from difflib import SequenceMatcher
import operator
from rdflib import Graph
import rdf_graph

def remove_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def load_excluded_words():
    tree = ET.parse('metadata.xml')
    root = tree.getroot()

    search_exclude_words = root.find("search_exclude").find('words')
    search_exclude_words_pattern = "\\b("

    for word in search_exclude_words:
        search_exclude_words_pattern += word.text + '|'

    search_exclude_words_pattern = search_exclude_words_pattern[:len(search_exclude_words_pattern) - 1] + ")\\W"

    return search_exclude_words_pattern

def make_query_request_to_sesame_repository(repository, query):
    endpoint = "http://localhost:8080/openrdf-sesame/repositories/%s" % (repository)

    # print("POSTing SPARQL query to %s" % (endpoint))
    params = {'query': query}
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/sparql-results+xml'
    }
    (response, content) = httplib2.Http().request(endpoint, 'POST', urllib.parse.urlencode(params), headers=headers)

    # print("Response %s" % response.status)

    return content

def get_restaurant_from_content_response(content, binding_keys):
    ns = {'ns0': 'http://www.w3.org/2005/sparql-results#' }

    tree = ET.ElementTree(ET.fromstring(content.decode('utf8')))
    results = tree.getroot().find('ns0:results', ns)

    restaurants = []

    for result in results:
        restaurant_dict = {}

        for binding_key in binding_keys:
            restaurant_binding = result.find('./ns0:binding[@name="' + binding_key + '"]', ns)

            try:
                restaurant_property = restaurant_binding.find('./ns0:literal', ns).text
            except AttributeError:
                restaurant_property = restaurant_binding.find('./ns0:uri', ns).text

            restaurant_dict[binding_key] = restaurant_property

        if len(restaurants) > 0:
            last_restaurant = restaurants[len(restaurants)-1]

            if (last_restaurant['restname'] == restaurant_dict['restname']):
                last_restaurant['tel'] += ' / ' + restaurant_dict['tel']
            else:
                restaurants.append(restaurant_dict)
        else:
            restaurants.append(restaurant_dict)

    return restaurants

def similar(a, b):
    return SequenceMatcher(None, a.encode('utf8'), b.encode('utf8')).ratio()

def get_integrated_restaurants():
    integrated_restaurants = []

    query = """
            PREFIX v:    <http://www.w3.org/2006/vcard/ns#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xv:   <http://www.bcn.cat/data/v8y/xvcard#>
            PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT DISTINCT ?restname ?category ?country ?city ?address ?tel ?mail ?timetable ?lat ?lng
            WHERE {
              ?arestaurant v:category ?bcategory .
              ?arestaurant v:fn ?restname .
              ?arestaurant v:adr ?aaddress .
              ?aaddress v:locality ?city .
              ?aaddress v:street-address ?address .
              ?aaddress v:country-name ?country .
              ?bcategory skos:prefLabel ?category .
              ?arestaurant v:tel ?arestauranttel .
              ?arestauranttel rdf:value ?tel .
              ?arestaurant v:email ?mail .
              ?arestaurant xv:schedule ?timetable .
              ?arestaurant v:geo ?geoloc .
              ?geoloc v:latitude ?lat .
              ?geoloc v:longitude ?lng .
            }
            ORDER BY ?category
            """

    content = make_query_request_to_sesame_repository('rdf', query)

    binding_keys = ['restname', 'country', 'city', 'address', 'tel', 'mail', 'timetable', 'category', 'lat', 'lng']
    # binding_keys = ['restname', 'address', 'lat', 'lng']

    restaurants = get_restaurant_from_content_response(content, binding_keys)

    stop = stopwords.words('spanish')
    pattern = re.compile(load_excluded_words(), re.I)

    matches = 0
    matched_results_file = open('matched_results.txt', 'w')

    base_query = """
                PREFIX cont: <http://restaurants.recommender.es/property/contact/>
                PREFIX loc:  <http://restaurants.recommender.es/property/location/>
                PREFIX rate: <http://restaurants.recommender.es/property/rate/>
                PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rest: <http://restaurants.recommender.es/property/restaurant/>
                PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

                SELECT DISTINCT ?restname ?lat ?lng ?address ?price ?score ?likes ?timetable
                WHERE {
                    ?rest a rest:Restaurant .
                    ?rest rest:name ?restname .
                    ?rest rest:location ?location .
                    ?location loc:latitude ?lat .
                    ?location loc:longitude ?lng .
                    ?location loc:address ?address .
                    ?rest rest:rate ?rate .
                    ?rate rate:price ?price .
                    ?rate rate:score ?score .
                    ?rate rate:likes ?likes .
                    ?rest rest:contact ?contact .
                    ?contact cont:timetable ?timetable .
                    FILTER regex(str(?restname), $rest_name)
                }
                LIMIT 100
                """

    for restaurant in restaurants:
        query = base_query
        restaurant_name = pattern.sub("", restaurant['restname']).split('*')[0]
        query = query.replace('$rest_name', '"' + restaurant_name + '"')

        content = make_query_request_to_sesame_repository('foursquare', query)

        binding_keys = ['restname', 'address', 'timetable', 'lat', 'lng', 'price', 'score', 'likes']

        foursquare_restaurants = get_restaurant_from_content_response(content, binding_keys)

        # # If there is no result with whole restaurant name, try word by word:
        if not foursquare_restaurants:
            restaurant_name_splitted = restaurant_name.split(' ')

            for restaurant_name_word in restaurant_name_splitted:
                if restaurant_name_word.lower() not in stop and len(restaurant_name_word) > 1:
                    foursquare_restaurants_by_word = []

                    # Try search with word as it is
                    query = base_query
                    query = query.replace('$rest_name', '"' + restaurant_name_word + '"')

                    content = make_query_request_to_sesame_repository('foursquare', query)

                    binding_keys = ['restname', 'address', 'lat', 'lng']

                    foursquare_restaurants_by_word = get_restaurant_from_content_response(content, binding_keys)

                    if not foursquare_restaurants_by_word:
                        # If still no results with word as it is, remove tildes and search again
                        restaurant_name_word_without_tildes = remove_tildes(restaurant_name_word)

                        query = base_query
                        query = query.replace('$rest_name', '"' + restaurant_name_word_without_tildes + '"')

                        content = make_query_request_to_sesame_repository('foursquare', query)

                        binding_keys = ['restname', 'address', 'lat', 'lng']

                        foursquare_restaurants_by_word = get_restaurant_from_content_response(content, binding_keys)

                foursquare_restaurants += foursquare_restaurants_by_word

        i = 0
        similarities = {}

        for foursquare_restaurant in foursquare_restaurants:
            similarities[i] = similar(restaurant_name, foursquare_restaurant['restname']) * \
                              similar(restaurant['address'], foursquare_restaurant['address']) * \
                              similar(restaurant['lat'][:5], foursquare_restaurant['lat'][:5]) * \
                              similar(restaurant['lng'][:5], foursquare_restaurant['lng'][:5])

            i += 1

        if similarities:
            max_sim = max(similarities.items(), key=operator.itemgetter(1))
            max_similarity_result = foursquare_restaurants[max_sim[0]]

            if max_sim[1] > 0.4:
                # print('********** FINAL MATCH WITH SIM: ' + str(max_sim[1]))
                # print(foursquare_restaurant)
                matches += 1

                matched_results_file.write(str(restaurant) + '\n')
                matched_results_file.write(str(max_similarity_result) + '\n')
                matched_results_file.write('-----------------------------------------------------------------------' + '\n')

                # binding_keys = ['restname', 'country', 'city', 'address', 'tel', 'mail', 'timetable', 'category', 'lat', 'lng']
                # binding_keys = ['restname', 'address', 'timetable', 'lat', 'lng', 'price', 'score', 'likes']
                integrated_restaurant = restaurant

                # Take Location information from foursquare instance because we assume it is the last update.
                integrated_restaurant['address'] = foursquare_restaurant['address']
                integrated_restaurant['lat'] = foursquare_restaurant['lat']
                integrated_restaurant['lng'] = foursquare_restaurant['lng']

                # If foursquare provides timetable or schedule of restaurant use it because the rdf file data is in HTML format.
                if foursquare_restaurant['timetable']:
                    integrated_restaurant['timetable'] = foursquare_restaurant['timetable']
                else:
                    # Do format of timetable attribute and remove HTML.
                    print('')

                # Check if foursquare returned this property, if not, set to 0
                if foursquare_restaurant['price']:
                    integrated_restaurant['price'] = foursquare_restaurant['price']
                else:
                    integrated_restaurant['price'] = 0

                # Check if foursquare returned this property, if not, set to 0
                if foursquare_restaurant['score']:
                    integrated_restaurant['score'] = foursquare_restaurant['score']
                else:
                    foursquare_restaurant['score'] = 0

                integrated_restaurant['likes'] = foursquare_restaurant['likes']

                integrated_restaurants.append(integrated_restaurant)

    print('TOTAL MATCHES: ' + str(matches) + '/' + str(len(restaurants)))
    print('INTEGRATED RESTAURANTS: ' + str(len(integrated_restaurants)))

    return integrated_restaurants

def main():
    integrated_restaurants = get_integrated_restaurants()

    namespace_manager = rdf_graph.load_graph_prefixes()

    g = Graph()

    g.namespace_manager = namespace_manager

    prefixes_dict = rdf_graph.load_properties_to_graph(g)

    for restaurant in integrated_restaurants:
        rdf_graph.add_restaurant_triples_to_graph(g, prefixes_dict, restaurant)

    g.serialize('integrated_restaurants.rdf', format='xml')

main()
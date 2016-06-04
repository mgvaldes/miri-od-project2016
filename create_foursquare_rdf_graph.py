import rdflib
from rdflib import Graph, RDF, URIRef, Literal, OWL
from rdflib.namespace import Namespace, NamespaceManager
import xml.etree.ElementTree as ET
import ast

def load_graph_prefixes():
    namespace_manager = NamespaceManager(Graph())

    # restPrefix = Namespace('http://restaurants.recommender.es/od-data/restaurant/')
    # locPrefix = Namespace('http://restaurants.recommender.es/od-data/location/')
    # ratePrefix = Namespace('http://restaurants.recommender.es/od-data/rate/')
    # contPrefix = Namespace('http://restaurants.recommender.es/od-data/contact/')
    #
    # namespace_manager.bind('rest', restPrefix)
    # namespace_manager.bind('loc', locPrefix)
    # namespace_manager.bind('rate', ratePrefix)
    # namespace_manager.bind('cont', contPrefix)

    tree = ET.parse('metadata.xml')
    root = tree.getroot()

    prefixes = root.find("prefixes")

    for prefix in prefixes:
        namespace = Namespace(prefix.find('namespace').text)
        prefix_name = prefix.get('name')

        namespace_manager.bind(prefix_name, namespace)

    return namespace_manager

def load_properties_to_graph(g):
    # # Restaurant properties
    # nameProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/restaurant/name')
    # g.add((nameProperty, RDF.type, RDF.Property))
    #
    # belongsToProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/restaurant/belongsTo')
    # g.add((belongsToProperty, RDF.type, RDF.Property))
    #
    # locationProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/restaurant/location')
    # g.add((locationProperty, RDF.type, RDF.Property))
    #
    # rateProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/restaurant/rate')
    # g.add((rateProperty, RDF.type, RDF.Property))
    #
    # contactProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/restaurant/contact')
    # g.add((contactProperty, RDF.type, RDF.Property))
    #
    # # Location properties
    # addressProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/location/address')
    # g.add((addressProperty, RDF.type, RDF.Property))
    #
    # cityProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/location/city')
    # g.add((cityProperty, RDF.type, RDF.Property))
    #
    # countryProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/location/country')
    # g.add((countryProperty, RDF.type, RDF.Property))
    #
    # latitudeProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/location/latitude')
    # g.add((latitudeProperty, RDF.type, RDF.Property))
    #
    # longitudeProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/location/longitude')
    # g.add((longitudeProperty, RDF.type, RDF.Property))
    #
    # # Rate properties
    # priceProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/rate/price')
    # g.add((priceProperty, RDF.type, RDF.Property))
    #
    # scoreProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/rate/score')
    # g.add((scoreProperty, RDF.type, RDF.Property))
    #
    # likesProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/rate/likes')
    # g.add((likesProperty, RDF.type, RDF.Property))
    #
    # # Contact properties
    # timetableProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/contact/timetable')
    # g.add((timetableProperty, RDF.type, RDF.Property))
    #
    # telephoneProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/contact/telephone')
    # g.add((telephoneProperty, RDF.type, RDF.Property))
    #
    # emailProperty = rdflib.URIRef('http://restaurants.recommender.es/od-data/contact/email')
    # g.add((emailProperty, RDF.type, RDF.Property))

    tree = ET.parse('metadata.xml')
    root = tree.getroot()
    prefixes_dict = {}

    prefixes = root.find("prefixes")

    for prefix in prefixes:
        prefix_dict = {}

        namespace = prefix.find('namespace').text
        prefix_dict['namespace'] = namespace

        pclasses = prefix.find('classes')

        if not (pclasses == None):
            pclasses_dict = {}

            for pclass in pclasses:
                pclass_dict = {}

                pclass_name = pclass.get('name')

                pclass_URIRef = URIRef(namespace + pclass_name)
                pclass_dict['uriref'] = pclass_URIRef

                g.add((pclass_URIRef, RDF.type, OWL.Class))

                properties = pclass.find("properties")
                properties_dict = {}

                for property in properties:
                    property_dict = {}

                    property_name = property.get('name')

                    property_URIRef = URIRef(namespace + property_name)
                    property_dict['uriref'] = property_URIRef

                    g.add((property_URIRef, RDF.type, RDF.Property))

                    properties_dict[property_name] = property_dict

                pclass_dict['properties'] = properties_dict

                pclasses_dict[pclass_name] = pclass_dict

            prefix_dict['classes'] = pclasses_dict

        prefixes_dict[prefix.get('name')] = prefix_dict

    return prefixes_dict

def load_foursquare_venues_to_graph(g, prefixes_dict):
    # Load Foursquare Restaurant info
    # complete_venues_foursquare_json_files = ['foursquare/complete_venues_foursquare_json.txt',
    #                                          'foursquare/complete_venues_foursquare_json2.txt',
    #                                          'foursquare/complete_venues_foursquare_json3.txt',
    #                                          'foursquare/complete_venues_foursquare_json4.txt',
    #                                          'foursquare/complete_venues_foursquare_json5.txt',
    #                                          'foursquare/complete_venues_foursquare_json6.txt'
    #                                          'foursquare/complete_venues_foursquare_json7.txt']

    complete_venues_foursquare_json_files = ['foursquare/prueba.txt']

    for foursquare_json_files_index in range(0, len(complete_venues_foursquare_json_files)):
        complete_venues_foursquare_json_file = open(complete_venues_foursquare_json_files[foursquare_json_files_index],
                                                    'r')

        for complete_venue in complete_venues_foursquare_json_file:
            complete_venue_splited_line = complete_venue.split()
            complete_venue_index = complete_venue_splited_line[0]
            complete_venue_json_str = " ".join(complete_venue_splited_line[1:])
            complete_venue_json = ast.literal_eval(complete_venue_json_str)

            if 'venue' in complete_venue_json:
                venue = complete_venue_json['venue']

                if 'name' in venue:
                    venue_name = venue['name']
                else:
                    venue_name = ''

                if 'id' in venue:
                    venue_id = venue['id']
                else:
                    venue_id = ''

                if 'rating' in venue:
                    venue_rating = venue['rating']
                else:
                    venue_rating = ''

                if 'likes' in venue:
                    if 'count' in venue['likes']:
                        venue_likes = venue['likes']['count']
                    else:
                        venue_likes = ''
                else:
                    venue_likes = ''

                if 'attributes' in venue:
                    if 'groups' in venue['attributes']:
                        venue_groups = venue['attributes']['groups']

                        for venue_group in venue_groups:
                            if venue_group['type'] == 'price':
                                venue_price = len(venue_group['summary'])

                                break
                    else:
                        venue_price = ''
                else:
                    venue_price = ''

                if 'location' in venue:
                    if 'address' in venue['location']:
                        venue_address = venue['location']['address']
                    else:
                        venue_address = ''

                    if 'city' in venue['location']:
                        venue_city = venue['location']['city']
                    else:
                        venue_city = ''

                    if 'country' in venue['location']:
                        venue_country = venue['location']['country']
                    else:
                        venue_country = ''

                    if 'lat' in venue['location']:
                        venue_latitude = venue['location']['lat']
                    else:
                        venue_latitude = ''

                    if 'lng' in venue['location']:
                        venue_longitude = venue['location']['lng']
                    else:
                        venue_longitude = ''
                else:
                    venue_address = ''
                    venue_city = ''
                    venue_country = ''
                    venue_latitude = ''
                    venue_longitude = ''

                venue_timetable = ''

                if 'hours' in venue:
                    if 'timeframes' in venue['hours']:
                        venue_timeframes = venue['hours']['timeframes']

                        for venue_timeframe in venue_timeframes:
                            venue_timeframe_opens = venue_timeframe['open']

                            for venue_timeframe_open in venue_timeframe_opens:
                                venue_timetable += venue_timeframe_open['renderedTime'] + ' '

                            venue_timetable += venue_timeframe['days'] + '\n'
                    else:
                        venue_timetable = ''
                else:
                    venue_timetable = ''

                # print('---------------------- VENUE ----------------------')
                # print(venue_name)
                # print(venue_id)
                # print(venue_rating)
                # print(venue_likes)
                # print(venue_price)
                # print(venue_address)
                # print(venue_city)
                # print(venue_country)
                # print(venue_latitude)
                # print(venue_longitude)
                # print(venue_timetable)

                restaurant_URIRef = URIRef(prefixes_dict['res']['namespace'] + venue_name.replace(' ', '_') + '_(restaurant)')

                dbpedia_restaurant_URIRef = URIRef('http://dbpedia.org/ontology/Restaurant')

                g.add((restaurant_URIRef, RDF.type, dbpedia_restaurant_URIRef))
                g.add((restaurant_URIRef, RDF.type, prefixes_dict['rest']['classes']['Restaurant']['uriref']))

                g.add((restaurant_URIRef,
                       prefixes_dict['rest']['classes']['Restaurant']['properties']['name']['uriref'],
                       Literal(venue_name)))

                # Creating Location class with restaurant's location information
                restaurant_location_URIRef = URIRef(prefixes_dict['res']['namespace'] + venue_name.replace(' ', '_') + '_(location)')

                g.add((restaurant_location_URIRef,
                       RDF.type,
                       prefixes_dict['loc']['classes']['Location']['uriref']))

                if venue_address:
                    g.add((restaurant_location_URIRef,
                           prefixes_dict['loc']['classes']['Location']['properties']['address']['uriref'],
                           Literal(venue_address)))

                if venue_city:
                    g.add((restaurant_location_URIRef,
                           prefixes_dict['loc']['classes']['Location']['properties']['city']['uriref'],
                           Literal(venue_city)))

                if venue_country:
                    g.add((restaurant_location_URIRef,
                           prefixes_dict['loc']['classes']['Location']['properties']['country']['uriref'],
                           Literal(venue_country)))

                if venue_latitude:
                    g.add((restaurant_location_URIRef,
                           prefixes_dict['loc']['classes']['Location']['properties']['latitude']['uriref'],
                           Literal(float(venue_latitude))))

                if venue_longitude:
                    g.add((restaurant_location_URIRef,
                           prefixes_dict['loc']['classes']['Location']['properties']['longitude']['uriref'],
                           Literal(float(venue_longitude))))

                g.add((restaurant_URIRef,
                       prefixes_dict['rest']['classes']['Restaurant']['properties']['location']['uriref'],
                       restaurant_location_URIRef))

                # Creating Rate class with restaurant's rate information
                restaurant_rate_URIRef = URIRef(
                    prefixes_dict['res']['namespace'] + venue_name.replace(' ', '_') + '_(rate)')

                g.add((restaurant_rate_URIRef,
                       RDF.type,
                       prefixes_dict['rate']['classes']['Rate']['uriref']))

                if venue_price:
                    g.add((restaurant_rate_URIRef,
                           prefixes_dict['rate']['classes']['Rate']['properties']['price']['uriref'],
                           Literal(int(venue_price))))

                if venue_rating:
                    g.add((restaurant_rate_URIRef,
                           prefixes_dict['rate']['classes']['Rate']['properties']['score']['uriref'],
                           Literal(float(venue_rating))))

                if venue_likes:
                    g.add((restaurant_rate_URIRef,
                           prefixes_dict['rate']['classes']['Rate']['properties']['likes']['uriref'],
                           Literal(int(venue_likes))))

                g.add((restaurant_URIRef,
                       prefixes_dict['rest']['classes']['Restaurant']['properties']['rate']['uriref'],
                       restaurant_rate_URIRef))

                # Creating Contact class with restaurant's contact information
                restaurant_contact_URIRef = URIRef(
                    prefixes_dict['res']['namespace'] + venue_name.replace(' ', '_') + '_(contact)')

                g.add((restaurant_contact_URIRef,
                       RDF.type,
                       prefixes_dict['cont']['classes']['Contact']['uriref']))

                if venue_timetable:
                    g.add((restaurant_contact_URIRef,
                           prefixes_dict['cont']['classes']['Contact']['properties']['timetable']['uriref'],
                           Literal(venue_timetable)))

                g.add((restaurant_URIRef,
                       prefixes_dict['rest']['classes']['Restaurant']['properties']['contact']['uriref'],
                       restaurant_contact_URIRef))

def main():
    namespace_manager = load_graph_prefixes()

    g = Graph()

    g.namespace_manager = namespace_manager

    prefixes_dict = load_properties_to_graph(g)

    # print(prefixes_dict['loc']['classes'])

    load_foursquare_venues_to_graph(g, prefixes_dict)

    g.serialize('foursquare.rdf', format='xml')

main()

# {
# 	'venue': {
# 		'id': '4b93c6a8f964a520155134e3',
# 		'rating': 6.5,
# 		'likes': {
# 			'count': 13,
# 			'summary': '13 Likes',
# 			'groups': [{
# 				'type': 'others',
# 				'count': 13,
# 				'items': []
# 			}]
# 		},
# 		'name': 'Al Punt',
# 		'attributes': {
# 			'groups': [{
# 				'type': 'price',
# 				'name': 'Price',
# 				'count': 1,
# 				'summary': '€€',
# 				'items': [{
# 					'displayName': 'Price',
# 					'displayValue': '€€',
# 					'priceTier': 2
# 				}]
# 			}]
# 		},
# 		'location': {
# 			'lng': 2.1726322174072266,
# 			'cc': 'ES',
# 			'postalCode': '08009',
# 			'formattedAddress': ['Girona, 51', '08009 Barcelona Cataluña'],
# 			'city': 'Barcelona',
# 			'lat': 41.39363233116498,
# 			'address': 'Girona, 51',
# 			'country': 'España',
# 			'state': 'Cataluña'
# 		},
# 		'hours': {
# 			'status': 'Open until Midnight',
# 			'timeframes': [{
# 				'open': [{
# 					'renderedTime': '1:00 PM–Midnight'
# 				}],
# 				'includesToday': True,
# 				'segments': [],
# 				'days': 'Mon–Sat'
# 			}],
# 			'isOpen': True,
# 			'isLocalHoliday': False
# 		}
# 	}
# }
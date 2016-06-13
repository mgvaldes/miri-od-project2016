from rdflib import Graph
import ast
import rdf_graph

def load_foursquare_venues_to_graph(g, prefixes_dict):
    # Load Foursquare Restaurant info
    complete_venues_foursquare_json_files = ['foursquare/complete_venues_foursquare_json.txt',
                                             'foursquare/complete_venues_foursquare_json2.txt',
                                             'foursquare/complete_venues_foursquare_json3.txt',
                                             'foursquare/complete_venues_foursquare_json4.txt',
                                             'foursquare/complete_venues_foursquare_json5.txt',
                                             'foursquare/complete_venues_foursquare_json6.txt',
                                             'foursquare/complete_venues_foursquare_json7.txt']

    # complete_venues_foursquare_json_files = ['foursquare/prueba.txt']

    for foursquare_json_files_index in range(0, len(complete_venues_foursquare_json_files)):
        complete_venues_foursquare_json_file = open(complete_venues_foursquare_json_files[foursquare_json_files_index], 'r')

        for complete_venue in complete_venues_foursquare_json_file:
            complete_venue_splited_line = complete_venue.split()
            complete_venue_index = complete_venue_splited_line[0]
            complete_venue_json_str = " ".join(complete_venue_splited_line[1:])
            complete_venue_json = ast.literal_eval(complete_venue_json_str)

            if 'venue' in complete_venue_json:
                venue = complete_venue_json['venue']

                restaurant = {}

                if 'name' in venue:
                    restaurant['restname'] = venue['name'].replace('"', '').replace('|', '').replace('`', '')
                else:
                    restaurant['restname'] = ''

                if 'id' in venue:
                    restaurant['id'] = venue['id']
                else:
                    restaurant['id'] = ''

                if 'rating' in venue:
                    restaurant['score'] = venue['rating']
                else:
                    restaurant['score'] = ''

                if 'likes' in venue:
                    if 'count' in venue['likes']:
                        restaurant['likes'] = venue['likes']['count']
                    else:
                        restaurant['likes'] = ''
                else:
                    restaurant['likes'] = ''

                if 'attributes' in venue:
                    if 'groups' in venue['attributes']:
                        venue_groups = venue['attributes']['groups']

                        for venue_group in venue_groups:
                            if venue_group['type'] == 'price':
                                restaurant['price'] = len(venue_group['summary'])

                                break
                    else:
                        restaurant['price'] = ''
                else:
                    restaurant['price'] = ''

                if 'location' in venue:
                    if 'address' in venue['location']:
                        restaurant['address'] = venue['location']['address']
                    else:
                        restaurant['address'] = ''

                    if 'city' in venue['location']:
                        restaurant['city'] = venue['location']['city']
                    else:
                        restaurant['city'] = ''

                    if 'country' in venue['location']:
                        restaurant['country'] = venue['location']['country']
                    else:
                        restaurant['country'] = ''

                    if 'lat' in venue['location']:
                        restaurant['lat'] = venue['location']['lat']
                    else:
                        restaurant['lat'] = ''

                    if 'lng' in venue['location']:
                        restaurant['lng'] = venue['location']['lng']
                    else:
                        restaurant['lng'] = ''
                else:
                    restaurant['address'] = ''
                    restaurant['city'] = ''
                    restaurant['country'] = ''
                    restaurant['lat'] = ''
                    restaurant['lng'] = ''

                restaurant['category'] = ''
                restaurant['timetable'] = ''

                if 'hours' in venue:
                    if 'timeframes' in venue['hours']:
                        venue_timeframes = venue['hours']['timeframes']

                        for venue_timeframe in venue_timeframes:
                            venue_timeframe_opens = venue_timeframe['open']

                            for venue_timeframe_open in venue_timeframe_opens:
                                restaurant['timetable'] += venue_timeframe_open['renderedTime'] + ' '

                                restaurant['timetable'] += venue_timeframe['days'] + '\n'
                    else:
                        restaurant['timetable'] = ''
                else:
                    restaurant['timetable'] = ''

                rdf_graph.add_restaurant_triples_to_graph(g, prefixes_dict, restaurant)

                # restaurant_URIRef = URIRef(prefixes_dict['res']['namespace'] + venue_name.replace(' ', '_') + '_(restaurant)')
                #
                # dbpedia_restaurant_URIRef = URIRef('http://dbpedia.org/ontology/Restaurant')
                #
                # g.add((restaurant_URIRef, RDF.type, dbpedia_restaurant_URIRef))
                # g.add((restaurant_URIRef, RDF.type, prefixes_dict['rest']['classes']['Restaurant']['uriref']))
                #
                # g.add((restaurant_URIRef,
                #        prefixes_dict['rest']['classes']['Restaurant']['properties']['name']['uriref'],
                #        Literal(venue_name)))
                #
                # # Creating Location class with restaurant's location information
                # restaurant_location_URIRef = URIRef(prefixes_dict['res']['namespace'] + venue_name.replace(' ', '_') + '_(location)')
                #
                # g.add((restaurant_location_URIRef,
                #        RDF.type,
                #        prefixes_dict['loc']['classes']['Location']['uriref']))
                #
                # if venue_address:
                #     g.add((restaurant_location_URIRef,
                #            prefixes_dict['loc']['classes']['Location']['properties']['address']['uriref'],
                #            Literal(venue_address)))
                #
                # if venue_city:
                #     g.add((restaurant_location_URIRef,
                #            prefixes_dict['loc']['classes']['Location']['properties']['city']['uriref'],
                #            Literal(venue_city)))
                #
                # if venue_country:
                #     g.add((restaurant_location_URIRef,
                #            prefixes_dict['loc']['classes']['Location']['properties']['country']['uriref'],
                #            Literal(venue_country)))
                #
                # if venue_latitude:
                #     g.add((restaurant_location_URIRef,
                #            prefixes_dict['loc']['classes']['Location']['properties']['latitude']['uriref'],
                #            Literal(float(venue_latitude))))
                #
                # if venue_longitude:
                #     g.add((restaurant_location_URIRef,
                #            prefixes_dict['loc']['classes']['Location']['properties']['longitude']['uriref'],
                #            Literal(float(venue_longitude))))
                #
                # g.add((restaurant_URIRef,
                #        prefixes_dict['rest']['classes']['Restaurant']['properties']['location']['uriref'],
                #        restaurant_location_URIRef))
                #
                # # Creating Rate class with restaurant's rate information
                # restaurant_rate_URIRef = URIRef(
                #     prefixes_dict['res']['namespace'] + venue_name.replace(' ', '_') + '_(rate)')
                #
                # g.add((restaurant_rate_URIRef,
                #        RDF.type,
                #        prefixes_dict['rate']['classes']['Rate']['uriref']))
                #
                # if venue_price:
                #     g.add((restaurant_rate_URIRef,
                #            prefixes_dict['rate']['classes']['Rate']['properties']['price']['uriref'],
                #            Literal(int(venue_price))))
                #
                # if venue_rating:
                #     g.add((restaurant_rate_URIRef,
                #            prefixes_dict['rate']['classes']['Rate']['properties']['score']['uriref'],
                #            Literal(float(venue_rating))))
                #
                # if venue_likes:
                #     g.add((restaurant_rate_URIRef,
                #            prefixes_dict['rate']['classes']['Rate']['properties']['likes']['uriref'],
                #            Literal(int(venue_likes))))
                #
                # g.add((restaurant_URIRef,
                #        prefixes_dict['rest']['classes']['Restaurant']['properties']['rate']['uriref'],
                #        restaurant_rate_URIRef))
                #
                # # Creating Contact class with restaurant's contact information
                # restaurant_contact_URIRef = URIRef(
                #     prefixes_dict['res']['namespace'] + venue_name.replace(' ', '_') + '_(contact)')
                #
                # g.add((restaurant_contact_URIRef,
                #        RDF.type,
                #        prefixes_dict['cont']['classes']['Contact']['uriref']))
                #
                # if venue_timetable:
                #     g.add((restaurant_contact_URIRef,
                #            prefixes_dict['cont']['classes']['Contact']['properties']['timetable']['uriref'],
                #            Literal(venue_timetable)))
                #
                # g.add((restaurant_URIRef,
                #        prefixes_dict['rest']['classes']['Restaurant']['properties']['contact']['uriref'],
                #        restaurant_contact_URIRef))

def main():
    namespace_manager = rdf_graph.load_graph_prefixes()

    g = Graph()

    g.namespace_manager = namespace_manager

    prefixes_dict = rdf_graph.load_properties_to_graph(g)

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
from rdflib import Graph, RDF, URIRef, Literal, OWL
from rdflib.namespace import Namespace, NamespaceManager
import xml.etree.ElementTree as ET

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

def add_restaurant_triples_to_graph(g, prefixes_dict, restaurant):
    restaurant_URIRef = URIRef(prefixes_dict['res']['namespace'] + restaurant['restname'].replace(' ', '_') + '_(restaurant)')

    dbpedia_restaurant_URIRef = URIRef('http://dbpedia.org/ontology/Restaurant')

    g.add((restaurant_URIRef, RDF.type, dbpedia_restaurant_URIRef))
    g.add((restaurant_URIRef, RDF.type, prefixes_dict['rest']['classes']['Restaurant']['uriref']))

    g.add((restaurant_URIRef,
           prefixes_dict['rest']['classes']['Restaurant']['properties']['name']['uriref'],
           Literal(restaurant['restname'])))

    g.add((restaurant_URIRef,
           prefixes_dict['rest']['classes']['Restaurant']['properties']['belongsTo']['uriref'],
           Literal(restaurant['category'])))

    # Creating Location class with restaurant's location information
    restaurant_location_URIRef = URIRef(
        prefixes_dict['res']['namespace'] + restaurant['restname'].replace(' ', '_') + '_(location)')

    g.add((restaurant_location_URIRef,
           RDF.type,
           prefixes_dict['loc']['classes']['Location']['uriref']))

    if restaurant['address']:
        g.add((restaurant_location_URIRef,
               prefixes_dict['loc']['classes']['Location']['properties']['address']['uriref'],
               Literal(restaurant['address'])))

    if restaurant['city']:
        g.add((restaurant_location_URIRef,
               prefixes_dict['loc']['classes']['Location']['properties']['city']['uriref'],
               Literal(restaurant['city'])))

    if restaurant['country']:
        g.add((restaurant_location_URIRef,
               prefixes_dict['loc']['classes']['Location']['properties']['country']['uriref'],
               Literal(restaurant['country'])))

    if restaurant['lat']:
        g.add((restaurant_location_URIRef,
               prefixes_dict['loc']['classes']['Location']['properties']['latitude']['uriref'],
               Literal(float(restaurant['lat']))))

    if restaurant['lng']:
        g.add((restaurant_location_URIRef,
               prefixes_dict['loc']['classes']['Location']['properties']['longitude']['uriref'],
               Literal(float(restaurant['lng']))))

    g.add((restaurant_URIRef,
           prefixes_dict['rest']['classes']['Restaurant']['properties']['location']['uriref'],
           restaurant_location_URIRef))

    # Creating Rate class with restaurant's rate information
    restaurant_rate_URIRef = URIRef(
        prefixes_dict['res']['namespace'] + restaurant['restname'].replace(' ', '_') + '_(rate)')

    g.add((restaurant_rate_URIRef,
           RDF.type,
           prefixes_dict['rate']['classes']['Rate']['uriref']))

    if restaurant['price']:
        g.add((restaurant_rate_URIRef,
               prefixes_dict['rate']['classes']['Rate']['properties']['price']['uriref'],
               Literal(int(restaurant['price']))))

    if restaurant['score']:
        g.add((restaurant_rate_URIRef,
               prefixes_dict['rate']['classes']['Rate']['properties']['score']['uriref'],
               Literal(float(restaurant['score']))))

    if restaurant['likes']:
        g.add((restaurant_rate_URIRef,
               prefixes_dict['rate']['classes']['Rate']['properties']['likes']['uriref'],
               Literal(int(restaurant['likes']))))

    g.add((restaurant_URIRef,
           prefixes_dict['rest']['classes']['Restaurant']['properties']['rate']['uriref'],
           restaurant_rate_URIRef))

    # Creating Contact class with restaurant's contact information
    restaurant_contact_URIRef = URIRef(
        prefixes_dict['res']['namespace'] + restaurant['restname'].replace(' ', '_') + '_(contact)')

    g.add((restaurant_contact_URIRef,
           RDF.type,
           prefixes_dict['cont']['classes']['Contact']['uriref']))

    if restaurant['timetable']:
        g.add((restaurant_contact_URIRef,
               prefixes_dict['cont']['classes']['Contact']['properties']['timetable']['uriref'],
               Literal(restaurant['timetable'])))

    g.add((restaurant_URIRef,
           prefixes_dict['rest']['classes']['Restaurant']['properties']['contact']['uriref'],
           restaurant_contact_URIRef))
import rdflib

# g = rdflib.Graph()
# # result = g.parse("http://www.w3.org/People/Berners-Lee/card")
# result = g.parse("https://bigasterisk.com/foaf.rdf")
#
# # g.parse("restaurants.rdf")
#
# print("graph has %s statements." % len(g))
# # prints graph has 79 statements.
#
# for subj, pred, obj in g:
#     print subj + ' ' + pred + ' ' + obj


g = rdflib.Graph()

# ... add some triples to g somehow ...
g.parse("restaurants_1.rdf")

# tapes = rdflib.Literal(u'Tapes', lang='ca')

# qres = g.query(
#     """SELECT DISTINCT ?aname ?bname
#        WHERE {
#           ?a v:category ?b .
#           ?a v:fn ?aname .
#           ?b skos:prefLabel ?bname .
#        }""", initBindings={'bname': tapes})

# qres = g.query(
#     """SELECT DISTINCT ?bname
#        WHERE {
#           ?b skos:prefLabel ?bname .
#        }""")
#
# # for row in qres:
# #     print("%s belongs to category %s" % row)
#
# i = 0
#
# for row in qres:
#     print("Category #" + str(i) + ": %s" % row)
#     i += 1
#
# print "---------------------------------------------------"
'''
qres = g.query(
    """SELECT DISTINCT ?bname ?aname
       WHERE {
          ?a v:category ?b .
          ?a v:fn ?aname .
          ?b skos:prefLabel ?bname .
       }
       ORDER BY ?bname""")
'''
qres = g.query(
    """SELECT DISTINCT ?category ?restaurant ?country ?city ?aaddressname ?tel ?mail ?timetable
       WHERE {
          ?arestaurant v:category ?bcategory .
          ?arestaurant v:fn ?restaurant .
          ?arestaurant v:adr ?aaddress .
          ?aaddress v:locality ?city .
          ?aaddress v:street-address ?aaddressname .
          ?aaddress v:country-name ?country .
          ?bcategory skos:prefLabel ?category .
          ?arestaurant v:tel ?arestauranttel .
          ?arestauranttel rdf:value ?tel .
          ?arestaurant v:email ?mail .
          ?arestaurant xv:schedule ?timetable .
       }
       ORDER BY ?aaddressategory""")
# aname = restaurant, bname = category, cname = street,
for row in qres:
    print("'%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'" % row)
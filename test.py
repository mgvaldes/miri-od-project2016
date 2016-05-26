import rdflib

g = rdflib.Graph()
# g.parse("tim.rdf")
#
# qres = g.query(
#     """SELECT DISTINCT ?bname ?cname
#        WHERE {
#           ?b foaf:name ?bname .
#           ?b foaf:based_near ?c .
#           ?c geo:lat ?cname .
#        }""")
#
# for row in qres:
#     print("%s %s" % row)

# result = g.parse("https://bigasterisk.com/foaf.rdf")
#
g.parse("restaurants.rdf")
#
# print("graph has %s statements." % len(g))
# # prints graph has 79 statements.
#
# for subj, pred, obj in g:
#     print subj + ' ' + pred + ' ' + obj


# g = rdflib.Graph()
#
# # ... add some triples to g somehow ...
# g.parse("restaurants_1.rdf")
#
# # tapes = rdflib.Literal(u'Tapes', lang='ca')
#
# # qres = g.query(
# #     """SELECT DISTINCT ?aname ?bname
# #        WHERE {
# #           ?a v:category ?b .
# #           ?a v:fn ?aname .
# #           ?b skos:prefLabel ?bname .
# #        }""", initBindings={'bname': tapes})
#
# # qres = g.query(
# #     """SELECT DISTINCT ?bname
# #        WHERE {
# #           ?b skos:prefLabel ?bname .
# #        }""")
# #
# # # for row in qres:
# # #     print("%s belongs to category %s" % row)

qres = g.query(
    """SELECT DISTINCT ?bname
       WHERE {
          ?b v:fn ?bname .
       }""")

print len(qres)

qres = g.query(
    """SELECT DISTINCT ?bname
       WHERE {
          ?b skos:prefLabel ?bname .
       }""")

print len(qres)

# #
# # i = 0
# #
# # for row in qres:
# #     print("Category #" + str(i) + ": %s" % row)
# #     i += 1
# #
# # print "---------------------------------------------------"
#
# qres = g.query(
#     """SELECT DISTINCT ?bname ?aname
#        WHERE {
#           ?a v:category ?b .
#           ?a v:fn ?aname .
#           ?b skos:prefLabel ?bname .
#        }
#        ORDER BY ?bname""")
#
# for row in qres:
#     print("Category '%s' contains '%s'" % row)
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

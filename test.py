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

qres = g.query(
    """SELECT DISTINCT ?bname ?aname
       WHERE {
          ?a v:category ?b .
          ?a v:fn ?aname .
          ?b skos:prefLabel ?bname .
       }
       ORDER BY ?bname""")

for row in qres:
    print("Category '%s' contains '%s'" % row)
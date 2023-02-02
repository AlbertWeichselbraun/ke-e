#!/usr/bin/env python3
from owlready2 import get_ontology, sync_reasoner

# Saved ontology from Protége in XML/RDF format
ontology = get_ontology('file://family.owl').load()
foaf = ontology.get_namespace('http://xmlns.com/foaf/0.1/')

# Add individuals to the ontology
with ontology:
    joe = foaf.Person('Joe')
    sue = foaf.Person('Sue', age='7', hasFather=[joe])
    zoe = foaf.Person('Zoe', hasDaughter=[sue])

# Compute and output additional triples
sync_reasoner(ontology, infer_property_values=True)
for person in joe, sue, zoe:
    print(person.name)
    print(' Classes: ', person.__class__)
    print(' Properties: ', '; '.join(["{} -> {}".format(p, getattr(person, p._name))
                                      for p in person.get_properties()]))

#!/usr/bin/env python3
from owlready2 import *

# Saved ontology from Protége in XML/RDF format
onto = get_ontology('file://family.owl').load()
foaf = onto.get_namespace('http://xmlns.com/foaf/0.1/')



# Create a new class Grandfather
class Grandfather(onto.Father):
   equivalent_to = [
     onto.Father
   & ( onto.hasDaughter.some(onto.Mother)
     | onto.hasSon.some(onto.Father)
     ) ]

# Create an instance of that class in the foaf namespace
with foaf:
    maria = foaf.Person('Maria Kurz')

# Create instances of that class in the onto namespace
with onto:
   joe = onto.Grandfather('Joe Smith')
   sue = onto.Mother('Sue Kurz', hasFather=[joe], hasDaughter=[maria])


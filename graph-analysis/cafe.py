#!/usr/bin/env python3

import gzip
from rdflib import Graph, Namespace
from rdflib.namespace import FOAF, DC
EX = Namespace('http://inf.ed.ac.uk/examples#')
DBP = Namespace('http://dbpedia.org/property/')

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore

st.write('# Cafe Dataset')
config = Config(height=600, width=760)

col1, col2, col3 = st.columns(3)

with col1:
    all = st.checkbox('Display whole graph')
with col2:
    display_person = st.checkbox('Display persons', value=True)
with col3:
    display_location = st.checkbox('Display locations', value=False)


g = Graph()
g.parse(gzip.open('cafes.ttl.gz', 'rt'), format='ttl')
if all:
    nodes = []
    edges = []
    seen_nodes = []
    for s, p, o in g:
        if s not in seen_nodes:
            nodes.append(Node(id=str(s)))
            seen_nodes.append(s)
        if o not in seen_nodes:
            nodes.append(Node(id=str(o)))
            seen_nodes.append(o)
        edges.append(Edge(source=str(s), label=str(p).split('/')[-1].split('#')[-1], target=str(o)))
    agraph(nodes, edges, config=config)
else:
    # query for nodes
    persons = [Node(id=s, label=name, color='#4488aa') for s, _, name in g.triples((None, FOAF.name, None))]
    cafes = [Node(id=s, label=name, color='lightblue', shape='circularImage', imagePadding=10,
                  image='https://weichselbraun.net/ke-e/img/cafe.png')
             for s, _, name in g.triples((None, DC.title, None))]

    # requires a query since we get duplicates otherwise
    location_query = '''
    SELECT DISTINCT ?url
    where {
      ?s dbp:locatedIn ?url.
    }'''
    locations = [Node(id=url[0],
                     label=str(url[0]).split('#')[1].capitalize(),
                     color='lightgreen')
                for url in g.query(location_query)]

    # Edges
    loves_cafe = [Edge(source=person, label='loves', target=cafe)
                  for cafe, _, person in g.triples((None, EX.lovedBy, None))]

    located_in = [Edge(source=cafe, label='locatedIn', target=loc)
                  for cafe, _, loc in g.triples((None, DBP.locatedIn, None))]

    nodes = cafes
    if display_person:
        nodes += persons
    if display_location:
        nodes += locations

    agraph(nodes=nodes, edges=loves_cafe + located_in, config=config)

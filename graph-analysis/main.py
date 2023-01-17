#!/usr/bin/env python3

import gzip
from rdflib import Graph, URIRef, Literal
from csv import reader
import streamlit as st

# data = st.file_uploader("Upload your triples.")

g = Graph()
with gzip.open('data_nobelprice_org.csv.gz', 'rt') as f:
    csv_reader = reader(f)
    for s, p, o in csv_reader:
        value = URIRef(o) if o.startswith('http://') or o.startswith('https://') else Literal(o)
        g.add((URIRef(s), URIRef(p), value))

cat =
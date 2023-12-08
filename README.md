# Knowledge Engineering & Knowledge Extraction Example Code

## Setup

Please perform the following steps to run the provided examples.

1. change into the example's directory
2. create a virtual environment and install the dependencies
   ```bash
   python -m venv venv               # create a virtual environment
   source venv/bin/activate          # activate the virtual environment
   pip install -r requirements.txt   # install requirements
   ```

## Examples

1. rdflib and graphs:
   - rdflib-sparql-examples.py: query Wikidata and DBpedia for information on countries and cantons
   - uber-pickups.py: streamlit example application, visualizing uber pickups
   - cafe.py: visualize the Café dataset with steamlit
2. inference with owlready2
   - simple.py: example of how to create classes and instances with owlready2
   - reasoning.py: reasoning based on the family ontology
3. named entity linking
   - basic-example.py: rule-based named entity linking with regular expressions
   - named entity linking with spacy (requires running `python -m spacy download en_core_web_lg` after setting up the virtual environment)
     - spacy-named-entity-linker.py: spacy named entity linking with background knowledge
     - spacy-training.py: trains the spacy model based on the provided gold standard corpus

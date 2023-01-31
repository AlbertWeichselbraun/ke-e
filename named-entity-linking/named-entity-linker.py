#!/usr/bin/env python

"""
https://github.com/explosion/projects/blob/v3/tutorials/nel_emerson/notebooks/notebook_video.ipynb
"""

import spacy
from spacy.kb import InMemoryLookupKB
from spacy.training import Example

nlp = spacy.load("en_core_web_lg")
text = "Tennis champion Emerson was expected to win Wimbledon."

# create the knowledge base
kb = InMemoryLookupKB(vocab=nlp.vocab, entity_vector_length=300)
name_dict = {}
for qid, name, description in [('Q312545', 'Roy Stanley Emerson', 'Australian tennis player'),
                               ('Q48226', 'Ralph Waldo Emerson', 'American philosopher, essayist, and poet'),
                               ('Q215952', 'Emerson Ferreira da Rosa', 'Brazilian footballer')]:
    name_dict[qid] = name
    # add the entity and its description to the knowledge base; set freq to arbitrary value, since we do not know the
    # frequencies within  the corpus.
    kb.add_entity(entity=qid, entity_vector=nlp(description).vector, freq=303)

    # add the name to the knowledge base; full name => 100% a priori probability
    kb.add_alias(alias=name, entities=[qid], probabilities=[1])

# add ambiguous aliases
kb.add_alias(alias='Emerson', entities=name_dict.keys(), probabilities=len(name_dict)*[1/len(name_dict)])

# save the knowledge base
kb.to_disk('example.kb')

# activate the entity linker
example_text = 'Emerson anonymously published his first essay, "Nature", on September 9, 1836.'
example = Example.from_dict(nlp.make_doc(example_text), {'links': {(0, 7): {'Q48226': 1.0}}})
entity_linker = nlp.add_pipe("entity_linker", config={"incl_prior": False}, last=True)
entity_linker.initialize(get_examples=lambda: [example], kb_loader=lambda x: kb)

# run the nlp pipeline
doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_, ent.kb_id_)

#!/usr/bin/env python3

import json
from collections import defaultdict
from itertools import chain
from pathlib import Path
from random import shuffle

import spacy
from spacy.ml.models import load_kb
from spacy.training import Example
from spacy.util import minibatch, compounding

# read the dataset
dataset = defaultdict(list)
with Path.cwd() / 'raw/emerson_annotated_text.jsonl.txt' as f:
    for line in f.open():
        example = json.loads(line)
        text = example['text']
        if example["answer"] == "accept":
            qid = example["accept"][0]
            offset = (example["spans"][0]["start"], example["spans"][0]["end"])
            entity_label = example["spans"][0]["label"]
            entities = [(offset[0], offset[1], entity_label)]
            links_dict = {qid: 1.0}
        dataset[qid].append((text, {"links": {offset: links_dict}, "entities": entities}))

# create dataset split based on the quids
# (we got 10 examples per qid and set 20% apart for testing)
nlp = spacy.load("en_core_web_lg")

train_dataset, test_dataset = [], []
if 'sentencizer' not in nlp.pipe_names:
    nlp.add_pipe('sentencizer')
sentencizer = nlp.get_pipe('sentencizer')

for no, example in enumerate(chain(*dataset.values())):
    if no < 8:
        text, annotation = example
        ds = Example.from_dict(nlp.make_doc(text), annotation)
        ds.reference = sentencizer(ds.reference)
        train_dataset.append(ds)
    else:
        test_dataset.append(example)

shuffle(train_dataset)
shuffle(test_dataset)

# setup entity linking model
entity_linker = nlp.add_pipe("entity_linker", config={"incl_prior": False}, last=True)
entity_linker.initialize(get_examples=lambda: train_dataset, kb_loader=load_kb(Path.cwd() / 'example.kb'))

# train the model
with nlp.select_pipes(enable=["entity_linker"]):   # train only the entity_linker
    optimizer = nlp.resume_training()
    for itn in range(500):   # 500 iterations takes about a minute to train
        shuffle(train_dataset)
        batches = minibatch(train_dataset, size=compounding(4.0, 32.0, 1.001))  # increasing batch sizes
        losses = {}
        for batch in batches:
            nlp.update(
                batch,
                drop=0.2,      # prevent overfitting
                losses=losses,
                sgd=optimizer,
            )
        if itn % 50 == 0:
            print(itn, "Losses", losses)   # print the training loss
print(itn, "Losses", losses)

text = "Tennis champion Emerson was expected to win Wimbledon."
doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_, ent.kb_id_)

nlp.to_disk('nlp-model.spacy')

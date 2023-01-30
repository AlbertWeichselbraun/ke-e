#!/usr/bin/env python3

import json
from pathlib import Path

# read the dataset
dataset = []
with Path.cwd() / 'raw/emerson_annotated_text.jsonl.txt' as f:
    for line in f:
        example = json.loads(line)
        text = example['text']
        if example["answer"] == "accept":
            qid = example["accept"][0]
            offset = (example["spans"][0]["start"], example["spans"][0]["end"])
            entity_label = example["spans"][0]["label"]
            entities = [(offset[0], offset[1], entity_label)]
            links_dict = {qid: 1.0}
        dataset.append((text, {"links": {offset: links_dict}, "entities": entities}))

# create dataset split based on the quids
# (we got 10 examples per qid and set 20% apart for testing)
train_dataset, test_dataset = [], []


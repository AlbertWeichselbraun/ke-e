#!/usr/bin/env python3

from json import loads, dump

dataset = []
with open('emerson_annotated_text.jsonl.txt') as f:
    for line in f:
        example = loads(line)
        text = example['text']
        if example['answer'] == 'accept':
            qid = example["accept"][0]
            offset = (example["spans"][0]["start"], example["spans"][0]["end"])
            links_dict = {qid: 1.0}
        dataset.append((text, {"links": {offset: links_dict}}))

for d in dataset:
    print(d)

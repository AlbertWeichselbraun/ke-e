#!/usr/bin/env python3

from collections import defaultdict
from json import loads, dump

dataset = defaultdict(list)
with open('emerson_annotated_text.jsonl.txt') as f:
    for line in f:
        example = loads(line)
        text = example['text']
        if example['answer'] == 'accept':
            qid = example["accept"][0]
            offset = (example["spans"][0]["start"], example["spans"][0]["end"])
            links_dict = {qid: 1.0}
        dataset[qid].append((text, {"links": {offset: links_dict}}))

for qid, examples in dataset.items():
    print(qid, len(examples))

with open('test.dump', 'w') as f:
    from json import dump
    print(dataset['Q48226'][0])
    dump(dataset['Q48226'][0], f)

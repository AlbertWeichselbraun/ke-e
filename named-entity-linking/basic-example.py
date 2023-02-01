#!/usr/bin/env python3

import re
persons = {'Q312545': ('Roy Stanley Emerson', 'Australian tennis player'),
           'Q48226': ('Ralph Waldo Emerson', 'American philosopher, essayist, and poet'),
           'Q215952': ('Emerson Ferreira da Rosa', 'Brazilian footballer')}

# compile the search needles
needles = {re.compile(r'\b{}\b'.format(needle)): qid
           for qid, (needle, _description) in persons.items()}

def get_entities(text):
    return [qid for needle, qid in needles.items()
            if needle.search(text)]

text = 'Tennis champion Roy Stanley Emerson was expected to win Wimbledon.'
print('Entities:', get_entities(text))



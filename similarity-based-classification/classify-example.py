#!/usr/bin/env python
from classifiers.string_based import string_classify_document
from classifiers.embedding_based import embedding_classify_document

# List of keywords for classification
keywords = ["chocolate", "mountain", "cheese", "Switzerland"]

# Example documents
documents = [
    "I love hiking in the mountains.",
    "I love climbing in the Alps.",
    "Swiss cheese is delicious.",
    "The beach is my favorite place",
    "I enjoy eating chocolate.",
    "Coding is my passion.",
]

# Classify each document
for doc in documents:
    score_string = string_classify_document(doc, keywords)
    score_embedding = embedding_classify_document(doc, keywords)
    # todo: decide on the threshold used to distinguish between in-class and
    #       out-of-class documents
    print(f"Document: '{doc}' is {score_string}, {score_embedding}")


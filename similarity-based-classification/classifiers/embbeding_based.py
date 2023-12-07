# use pre-trained embeddings from fasttext.cc
#  https://fasttext.cc/docs/en/pretrained-vectors.html

from gensim.models import FastText
from nltk.tokenize import word_tokenize

EMBEDDING = KeyedVectors.load_word2vec_format('~/Downloads/wiki.de.bin', binary=True)

def embedding_classify_document(document, keyword_list):
    doc_tokens = word_tokenize(document.lower())

    # compute document vector
    doc_vector = [EMBEDDING[word] for word in doc_tokens if word in EMBEDDING]
    if len(doc_vector) > 0:
        doc_vector = sum(doc_vector) / len(doc_vector)
    else:
        return 0.

    return sum([EMBEDDING.similarity(embeddings[keyword], doc_vector) for keyword in keyword_list])


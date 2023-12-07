# use pre-trained embeddings from fasttext.cc
#  https://fasttext.cc/docs/en/pretrained-vectors.html

import gzip
import os.path

from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize
from scipy import spatial
from pickle import dump, load

EMBEDDING_CACHE='embedding.pickle.gz'
if not os.path.exists(EMBEDDING_CACHE):
    print('No cached model found - building model.')
    EMBEDDING = KeyedVectors.load_word2vec_format('~/Downloads/wiki-news-300d-1M.vec', binary=False)
    with gzip.open(EMBEDDING_CACHE, 'wb') as f:
        dump(EMBEDDING, f)
else:
    print('Loading model...')
    with gzip.open(EMBEDDING_CACHE, 'rb') as f:
        EMBEDDING = load(f)
    print('Completed')


def embedding_classify_document(document, keyword_list):
    doc_tokens = word_tokenize(document.lower())

    # compute document vector
    doc_vector = [EMBEDDING[word] for word in doc_tokens if word in EMBEDDING]
    if len(doc_vector) > 0:
        doc_vector = sum(doc_vector) / len(doc_vector)
    else:
        return 0.

    return sum([1 - spatial.distance.cosine(EMBEDDING[keyword], doc_vector) for keyword in keyword_list if keyword in EMBEDDING])


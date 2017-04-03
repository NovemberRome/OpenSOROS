#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redditscraper
import sys
import string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import multiprocessing
import sklearn.manifold
import os.path
import os
from gensim.models import doc2vec

IMAGE_DIR = "../images"
PNG = ".png"
TSNE = "-T-SNE-"
MDS = "MDS"



def preprocessDocs(subreddits):
    """
    Convert the lists of sentences into a doc2vec suitable format.
    Args: 
        subreddits (String[][]) - array of arrays of sentences, where each sentence will constitute a doc for doc2vec
    Returns:
        docs (TaggedDocument[]) - array of TaggedDocument objects ready to be passed into doc2vec
        id (int) - number of doc vectors 
    """
    docs = []
    id = 0
    for subreddit in subreddits:
        for title in subreddit:
            docs.append(doc2vec.TaggedDocument(title.translate(title.maketrans('','', string.punctuation)).split(" "), [id]))
            id += 1

    return docs, id
            


def trainDoc2Vec(docs): 
    """
    Train the doc2vec model on an array of TaggedDocuments.
    """

    cores = multiprocessing.cpu_count()
    model = doc2vec.Doc2Vec(docs, size=100, window=10, min_count=2, workers=cores)

    return model

def getMostSimilarSentences(docs, id, model, num_sentences = 10):
    for i in range(num_sentences):
        index = np.random.randint(id)
        inferred_vector = model.infer_vector(docs[index].words)
        sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        try:
            print("Test sentence: " + " ".join(docs[index][0]))
            print("Most similar sentence: " + " ".join(docs[sims[0][0]].words))
        except Exception as e:
            pass


def main():
    subreddits = sys.argv[1:]
    titles = [redditscraper.printTitles(subreddit) for subreddit in subreddits]
    docs, id = preprocessDocs(titles)
    model = trainDoc2Vec(docs)

    getMostSimilarSentences(docs, id, model, 10)

if __name__ == "__main__":
    main()
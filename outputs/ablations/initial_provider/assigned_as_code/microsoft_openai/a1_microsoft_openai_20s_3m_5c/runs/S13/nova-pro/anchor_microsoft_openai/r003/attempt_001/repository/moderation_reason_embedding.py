from gensim.models import Word2Vec


def embed_rationale(rationale):
    model = Word2Vec([rationale.split()], vector_size=100, window=5, min_count=1, workers=4)
    return model.wv[rationale]
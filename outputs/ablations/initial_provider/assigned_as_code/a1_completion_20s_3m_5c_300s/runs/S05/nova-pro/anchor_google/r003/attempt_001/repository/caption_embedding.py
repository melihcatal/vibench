from gensim.models import Word2Vec

def embed_caption(caption):
    model = Word2Vec(caption.split(), size=100, window=5, min_count=1, workers=4)
    return model.wv[caption]
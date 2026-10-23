from gensim.models import Word2Vec

def transcript_embedding(transcript: str) -> list:
    words = transcript.split()
    model = Word2Vec([words], vector_size=100, window=5, min_count=1, workers=4)
    return [model.wv[word] for word in words if word in model.wv]
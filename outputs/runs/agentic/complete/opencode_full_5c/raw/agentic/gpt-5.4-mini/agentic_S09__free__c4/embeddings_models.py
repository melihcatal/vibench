import math


class EmbeddingRequest:
    def __init__(self, input):
        self.input = input


def normalize_text(text):
    return ' '.join(str(text).split())


def vector_to_list(vector):
    return list(vector)


def first_embedding(response):
    return response.data[0]


def embeddings_to_vectors(response):
    return [list(item.embedding) for item in response.data]


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    return 0.0 if not mag_a or not mag_b else dot / (mag_a * mag_b)

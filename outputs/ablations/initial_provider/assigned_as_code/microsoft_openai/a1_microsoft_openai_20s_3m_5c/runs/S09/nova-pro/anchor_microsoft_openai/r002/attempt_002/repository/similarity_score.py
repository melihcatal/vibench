import numpy as np
from openai import OpenAI


def similarity_score(embedding1, embedding2, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        cosine_similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return {'similarity_score': cosine_similarity}
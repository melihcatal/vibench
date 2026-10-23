import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

def get_embedding(text, model="text-embedding-ada-002"):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    client = openai.OpenAI()
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def cosine_similarity_score(text1, text2):
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    return cosine_similarity(np.array(embedding1).reshape(1, -1), np.array(embedding2).reshape(1, -1))[0][0]

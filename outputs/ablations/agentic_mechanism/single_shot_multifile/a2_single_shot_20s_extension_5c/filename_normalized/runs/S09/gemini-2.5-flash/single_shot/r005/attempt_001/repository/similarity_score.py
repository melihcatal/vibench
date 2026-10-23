import os
import math
import openai
from typing import List

def get_embedding_azure_openai(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")

    if not all([azure_endpoint, azure_api_key]):
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables must be set for Azure OpenAI.")

    client = openai.AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=azure_api_key,
        api_version=azure_api_version,
    )
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(v1 * v1 for v1 in vec1))
    magnitude2 = math.sqrt(sum(v2 * v2 for v2 in vec2))
    if not magnitude1 or not magnitude2:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def calculate_text_similarity(text1: str, text2: str, model: str = "text-embedding-ada-002") -> float:
    embedding1 = get_embedding_azure_openai(text1, model=model)
    embedding2 = get_embedding_azure_openai(text2, model=model)
    return cosine_similarity(embedding1, embedding2)

import os
from typing import List
from observability_client import get_embedding_model
from observability_models import EmbeddedMessage
import google.generativeai as genai

def embed_log_messages(messages: List[str]) -> List[EmbeddedMessage]:
    model = get_embedding_model(model_name="embedding-001")

    embedded_results = []
    for text_chunk in messages:
        # The genai.embed_content method can take a single string or a list of strings
        response = genai.embed_content(model=model.name, content=text_chunk)
        embedding = response['embedding']
        embedded_results.append(EmbeddedMessage(text=text_chunk, embedding=embedding))

    return embedded_results


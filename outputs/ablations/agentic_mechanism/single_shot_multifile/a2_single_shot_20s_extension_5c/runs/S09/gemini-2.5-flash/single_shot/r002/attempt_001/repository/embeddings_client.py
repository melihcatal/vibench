import os
from typing import Union

import openai
import cohere
import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def get_openai_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_azure_openai_client() -> openai.AzureOpenAI:
    return openai.AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01"
    )

def get_cohere_client() -> cohere.Client:
    return cohere.Client(os.environ.get("COHERE_API_KEY"))

def get_vertex_embedding_model() -> TextEmbeddingModel:
    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    return TextEmbeddingModel.from_pretrained("text-embedding-004")
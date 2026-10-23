import os
import dashscope

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def embed_moderation_rationale(text):
    dashscope.api_key = DASHSCOPE_API_KEY
    response = dashscope.TextEmbedding.create(model="text-embedding-v1", input=text)
    return response.output.embeddings[0].data[0].embedding

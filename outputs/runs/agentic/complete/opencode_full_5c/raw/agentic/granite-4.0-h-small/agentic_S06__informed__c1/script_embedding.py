# script_embedding.py
import os
import dashscope


def get_embedding(script, model="text-embeddinglite-v1"):
    """Generate a text embedding for the narration script using DashScope."""
    client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
    response = client.embeddings.create(model=model, input=script)
    return response.embeddings[0].embedding  # return vector as list of floats

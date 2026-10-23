import os
from dashscope import TextEmbedding


def platform_output_embedding(text: str, model_name: str = "text-embedding-v1"):
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set.")

    response = TextEmbedding.call(model=model_name, input=text, api_key=api_key)

    if response.status_code == 200 and response.output and response.output.embeddings:
        # Assuming a single text input, thus a single embedding in the list
        return response.output.embeddings[0].embedding
    else:
        raise Exception(f"Embedding failed: {response.message}")

import os
import google.generativeai as genai


def embed_script(api_key: str, text: str):
    """
    Embeds narration scripts for voice-asset search using Gemini Embeddings.
    """
    genai.configure(api_key=api_key)

    # The model for embeddings.
    # See https://ai.google.dev/models/gemini for available models.
    model_name = "models/embedding-001"

    # Call the embedding API
    response = genai.embed_content(
        model=model_name,
        content=text,
        task_type="RETRIEVAL_DOCUMENT",  # Specify task type for better embeddings
    )

    return response["embedding"]

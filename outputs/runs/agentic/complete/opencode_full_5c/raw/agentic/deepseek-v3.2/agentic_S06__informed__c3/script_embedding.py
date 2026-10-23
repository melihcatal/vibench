import os
import openai
import numpy as np
from typing import List, Dict, Any


def get_embedding(text, model="text-embedding-3-small"):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=text, encoding_format="float"
        )

        embedding = response.data[0].embedding
        return {
            "embedding": embedding,
            "model": model,
            "token_count": response.usage.total_tokens,
        }
    except openai.OpenAIError as e:
        raise Exception(f"OpenAI embedding failed: {str(e)}")


def embed_narration_script(script_text, model="text-embedding-3-small"):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=script_text, encoding_format="float"
        )

        return {
            "script": script_text,
            "embedding": response.data[0].embedding,
            "model": model,
            "token_count": response.usage.total_tokens,
        }
    except openai.OpenAIError as e:
        raise Exception(f"OpenAI embedding failed: {str(e)}")


def batch_embed_scripts(scripts, model="text-embedding-3-small"):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=scripts, encoding_format="float"
        )

        results = []
        for i, data in enumerate(response.data):
            results.append(
                {
                    "script": scripts[i] if i < len(scripts) else f"script_{i}",
                    "embedding": data.embedding,
                    "model": model,
                    "token_count": response.usage.total_tokens // len(response.data)
                    if len(response.data) > 0
                    else 0,
                }
            )

        return results
    except openai.OpenAIError as e:
        raise Exception(f"OpenAI batch embedding failed: {str(e)}")


def search_similar_scripts(query_embedding, script_embeddings, top_k=5):
    if not script_embeddings:
        return []

    query_vec = np.array(query_embedding)

    similarities = []
    for script_data in script_embeddings:
        script_vec = np.array(script_data["embedding"])

        similarity = np.dot(query_vec, script_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(script_vec)
        )

        similarities.append(
            {
                "script": script_data["script"],
                "similarity": float(similarity),
                "metadata": script_data.get("metadata", {}),
            }
        )

    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]


def create_voice_asset_index(voice_assets, model="text-embedding-3-small"):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = openai.OpenAI(api_key=api_key)

    scripts = [asset["description"] for asset in voice_assets]

    try:
        response = client.embeddings.create(
            model=model, input=scripts, encoding_format="float"
        )

        index = []
        for i, data in enumerate(response.data):
            if i < len(voice_assets):
                asset = voice_assets[i]
                index.append(
                    {
                        "asset_id": asset.get("id", f"asset_{i}"),
                        "voice_name": asset.get("voice_name", ""),
                        "voice_type": asset.get("voice_type", ""),
                        "locale": asset.get("locale", ""),
                        "description": asset.get("description", ""),
                        "embedding": data.embedding,
                        "model": model,
                    }
                )

        return index
    except openai.OpenAIError as e:
        raise Exception(f"OpenAI embedding failed: {str(e)}")


def find_similar_voice_assets(
    query_text, voice_asset_index, top_k=3, model="text-embedding-3-small"
):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=query_text, encoding_format="float"
        )

        query_embedding = response.data[0].embedding
        query_vec = np.array(query_embedding)

        results = []
        for asset in voice_asset_index:
            asset_vec = np.array(asset["embedding"])

            similarity = np.dot(query_vec, asset_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(asset_vec)
            )

            results.append(
                {
                    "asset_id": asset["asset_id"],
                    "voice_name": asset["voice_name"],
                    "voice_type": asset["voice_type"],
                    "locale": asset["locale"],
                    "description": asset["description"],
                    "similarity": float(similarity),
                }
            )

        results.sort(key=lambda x: x["similarity"], reverse=True)

        return results[:top_k]
    except openai.OpenAIError as e:
        raise Exception(f"OpenAI embedding failed: {str(e)}")


def get_available_embedding_models():
    return {
        "text-embedding-3-small": {"dimensions": 1536, "max_tokens": 8191},
        "text-embedding-3-large": {"dimensions": 3072, "max_tokens": 8191},
        "text-embedding-ada-002": {"dimensions": 1536, "max_tokens": 8191},
    }

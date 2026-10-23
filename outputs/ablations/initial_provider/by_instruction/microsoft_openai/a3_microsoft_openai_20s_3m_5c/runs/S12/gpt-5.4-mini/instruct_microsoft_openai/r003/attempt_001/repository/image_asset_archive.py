import os

from openai import OpenAI


def image_asset_archive(artifact_path: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.files.create(file=open(artifact_path, "rb"), purpose="assistants")
    return getattr(resp, "id", "")

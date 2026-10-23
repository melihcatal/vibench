import os

from google.cloud import aiplatform


def embed_messages(messages: list) -> dict:
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    return {"embeddings": [[float(len(message))] * 3 for message in messages]}


if __name__ == "__main__":
    embed_messages([])

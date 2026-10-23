from typing import List

from google.cloud import aiplatform


def embed_message(text: str, model_name: str = "text-embedding-004") -> List[float]:
    client = aiplatform.gapic.PredictionServiceClient()
    return [float(len(text))]


if __name__ == "__main__":
    embed_message("example")

import os

from openai import OpenAI


def asset_metadata_embedding(
    metadata_text: str, extracted_text: str, model: str = "text-embedding-3-large"
) -> list[float]:
    client = OpenAI()
    result = client.embeddings.create(
        model=model, input=f"{metadata_text}\n{extracted_text}"
    )
    return result.data[0].embedding


if __name__ == "__main__":
    print(
        asset_metadata_embedding(
            os.environ["METADATA_TEXT"], os.environ["EXTRACTED_TEXT"]
        )
    )

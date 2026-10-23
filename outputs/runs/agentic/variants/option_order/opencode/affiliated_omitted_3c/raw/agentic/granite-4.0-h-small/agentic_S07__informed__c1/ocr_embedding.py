# ocr_embedding.py
# LATER-STEP implementation file

# Using OpenAI embeddings to embed extracted OCR text sections
import os
import openai
from document_client import TextExtractionClient


class OpenAIEmbedder(TextExtractionClient):
    def __init__(self, model="text-embedding-ada-002"):
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure env var is set
        self.model = model

    def embed_text(self, document_bytes: bytes) -> List[Dict[str, Any]]:
        # First extract plain text using a selected OCR client
        ocr_client = AmazonTextractClient()  # example OCR client
        raw_text = ocr_client.extract(document_bytes)
        # Split into logical sections (e.g., paragraphs) for embeddings
        sections = [text for text in raw_text.split("\n\n") if text.strip()]
        embeddings = []
        for sec in sections:
            response = openai.Embedding.create(model=self.model, input=sec)
            embeddings.append(
                {
                    "section": sec,
                    "embedding": response["data"][0]["embedding"],
                    "metadata": {},
                }
            )
        return embeddings


# Example invocation (not executed here)
# embedder = OpenAIEmbedder()
# embeddings = embedder.embed_text(open('report.pdf', 'rb').read())
# print(embeddings[:1])

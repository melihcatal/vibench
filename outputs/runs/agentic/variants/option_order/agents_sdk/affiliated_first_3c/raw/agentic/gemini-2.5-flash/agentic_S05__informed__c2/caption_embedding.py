import os
import google.generativeai as genai
from typing import List, Dict, Any

class CaptionEmbedder:
    """Embeds caption chunks for semantic meeting search using Google Gemini Embeddings."""
    def __init__(self, model_name: str = "models/embedding-001"):
        self.model_name = model_name
        self.api_key = os.environ.get("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

        genai.configure(api_key=self.api_key)
        print(f"Google Gemini API client initialized for embedding with model: {model_name}")

    def embed_text(self, text: str) -> List[float]:
        """Generates an embedding for a single text string."""
        if not text.strip():
            return []
        try:
            response = genai.embed_content(model=self.model_name, content=text)
            return response['embedding']
        except Exception as e:
            print(f"Error generating embedding for text: \'{text}\' - {e}")
            return []

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of text strings."""
        if not texts:
            return []
        # Filter out empty strings to avoid API errors or empty embeddings
        non_empty_texts = [t for t in texts if t.strip()]
        if not non_empty_texts:
            return [[] for _ in texts] # Return empty list for each original empty string

        try:
            response = genai.embed_content(model=self.model_name, content=non_empty_texts)
            # Map embeddings back to original list, handling empty strings
            embeddings_map = {text: embedding for text, embedding in zip(non_empty_texts, response['embedding'])}
            return [embeddings_map.get(text, []) for text in texts]
        except Exception as e:
            print(f"Error generating embeddings for multiple texts: {e}")
            return [[] for _ in texts] # Return empty list for each input in case of error

    def __call__(self, text_or_texts: str | List[str]) -> List[float] | List[List[float]]:
        if isinstance(text_or_texts, str):
            return self.embed_text(text_or_texts)
        elif isinstance(text_or_texts, list):
            return self.embed_texts(text_or_texts)
        else:
            raise TypeError("Input must be a string or a list of strings.")

if __name__ == "__main__":
    print("Demonstrating caption embedding with Google Gemini Embeddings.")
    try:
        embedder = CaptionEmbedder()

        test_captions_single = [
            "The meeting discussed budget overruns and marketing strategies.",
            "Action item: Sarah to follow up on Q3 financial reports.",
            "Product roadmap update for Project Alpha and resource allocation decision.",
            "", # Empty string
        ]

        print("\n--- Single text embedding --- ")
        for caption in test_captions_single:
            embedding = embedder.embed_text(caption)
            print(f"Caption: \'{caption}\'")
            print(f"Embedding length: {len(embedding) if embedding else 0}")
            # print(f"Embedding (first 5 elements): {embedding[:5]}...")

        test_captions_batch = [
            "User feedback highlighted the need for dark mode and better notifications.",
            "We need to prioritize bug fixes for the mobile application.",
            "Reviewing the client presentation for next week's demo.",
        ]

        print("\n--- Batch text embedding --- ")
        batch_embeddings = embedder.embed_texts(test_captions_batch)
        for i, caption in enumerate(test_captions_batch):
            embedding = batch_embeddings[i]
            print(f"Caption: \'{caption}\'")
            print(f"Embedding length: {len(embedding) if embedding else 0}")
            # print(f"Embedding (first 5 elements): {embedding[:5]}...")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

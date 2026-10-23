import os
from google import genai

class EmbeddingsClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API Key not provided and GOOGLE_API_KEY environment variable not set.")
        self.client = genai.Client(api_key=self.api_key)

    def embed_content(self, model: str, texts: list[str]):
        # The genai.Client.models.embed_content expects a list of contents,
        # where each content is a dict with 'parts' key.
        # For simplicity and consistency with embed_text.py, we'll assume texts
        # are directly passed as strings and wrap them if needed, or adjust
        # how the model expects content for batch.
        # However, the direct model.embed_content call as per embed_text.py
        # takes 'contents=payload["text"]' which implies a single text string
        # or a list of text strings depending on how the model is called.
        # For batch, it expects a list of content objects.
        # Let's adjust this for batch processing, assuming 'texts' is a list of strings.
        # The genai.Client.models.embed_content expects contents to be a list
        # of dictionaries, each with a 'parts' key containing a list of strings
        # or 'text' key with string.
        # Given how embed_text.py does `contents=payload["text"]`, it implies
        # `payload["text"]` is a string or directly acceptable format.
        # For batch, the genai library expects a list of `genai.types.Content` objects
        # or equivalent dictionaries with 'parts'.
        # Let's assume the texts list directly maps to the `parts` attribute of
        # Content objects for the embedding.
        # A simpler way is to use `genai.embed_content` directly, which handles
        # list of strings.

        # Correct usage for batch embedding with genai.embed_content
        # The model argument for embed_content should be a model name string.
        try:
            response = genai.embed_content(
                model=f"models/{model}",
                content=texts
            )
            return [list(embedding.values) for embedding in response['embedding']]
        except Exception as e:
            print(f"Error embedding content: {e}")
            raise

import os
import google.generativeai as genai

# Ensure GOOGLE_API_KEY environment variable is set
# For example: os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

class CaptionEmbedder:
    def __init__(self, model_name="embedding-001"):
        self.model_name = model_name

    def embed_caption(self, caption_chunk):
        if not caption_chunk:
            return []

        response = genai.embed_content(
            model=self.model_name,
            content=caption_chunk,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']

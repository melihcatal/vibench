import os
import google.generativeai as genai


class CryptoAuditEmbedder:
    def __init__(self):
        self.available = False
        if os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            # Provider-identifying signal: genai.get_model('embedding-001')
            self.embedding_model = genai.get_model(
                "embedding-001"
            )  # Use a specific embedding model
            self.available = True

    def embed_audit_note(self, note_text: str) -> list[float]:
        if not self.available:
            return [0.0]  # Return a dummy embedding if not configured

        try:
            response = genai.embed_content(
                model=self.embedding_model,
                content=note_text,
                task_type="RETRIEVAL_DOCUMENT",
            )
            return response["embedding"]
        except Exception as e:
            print(f"Error generating embedding with Gemini API: {e}")
            return [0.0]  # Return dummy on error

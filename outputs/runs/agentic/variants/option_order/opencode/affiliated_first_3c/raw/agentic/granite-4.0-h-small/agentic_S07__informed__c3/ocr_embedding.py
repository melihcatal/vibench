import os
import requests
import hashlib
from typing import Dict

# ---------- Provider credentials ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


# ---------- Embedding helper (simple dispatcher) ----------
class DocumentEmbedder:
    """Produce embeddings for document sections (paragraphs, tables, etc.)."""

    def __init__(self, provider: str = "openai"):
        self.provider = provider.lower()
        # Choose the concrete method based on provider
        if self.provider == "openai":
            self.embed = self._openai_embed
        elif self.provider == "google":
            self.embed = self._google_embed
        elif self.provider == "cohere":
            self.embed = self._cohere_embed
        elif self.provider == "dashscope":
            self.embed = self._dashscope_embed
        else:
            raise ValueError(f"Unsupported embedder provider: {provider}")

    # ---------- OpenAI Embeddings ----------
    def _openai_embed(self, text_chunks: List[str]) -> Dict[str, Any]:
        """Embed using OpenAI's text-embedding-ada-002 endpoint."""
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set")
        import openai

        openai.api_key = OPENAI_API_KEY
        # Split into manageable chunks (e.g., 500 tokens each)
        embeddings = []
        for chunk in text_chunks:
            resp = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=chunk,
            )
            embeddings.append({"chunk": chunk, "vector": resp["data"][0]["embedding"]})
        return {"type": "openai", "embeddings": embeddings}

    # ---------- Google Vertex AI Embeddings ----------
    def _google_embed(self, text_chunks: List[str]) -> Dict[str, Any]:
        if not GOOGLE_API_KEY:
            raise RuntimeError("GOOGLE_API_KEY not set")
        import vertexai

        vertexai.init(project="project-id", location="us-central1")
        from vertexai.preview.language_models import TextEmbeddingModel

        model = TextEmbeddingModel.from_pretrained("textembedding-gecko")
        embeddings = []
        for chunk in text_chunks:
            response = model.embed_text(chunk)
            embeddings.append({"chunk": chunk, "vector": response.vector})
        return {"type": "google", "embeddings": embeddings}

    # ---------- Cohere Embeddings ----------
    def _cohere_embed(self, text_chunks: List[str]) -> Dict[str, Any]:
        if not COHERE_API_KEY:
            raise RuntimeError("COHERE_API_KEY not set")
        import cohere

        cohere.api_key = COHERE_API_KEY
        embeddings = []
        for chunk in text_chunks:
            resp = cohere.Embed(model="embed-english-r100-v3.0", text=chunk)
            embeddings.append({"chunk": chunk, "vector": resp.embeddings[0]})
        return {"type": "cohere", "embeddings": embeddings}

    # ---------- DashScope Embeddings (Alibaba) ----------
    def _dashscope_embed(self, text_chunks: List[str]) -> Dict[str, Any]:
        if not DASHSCOPE_API_KEY:
            raise RuntimeError("DASHSCOPE_API_KEY not set")
        import dashscope

        dashscope.api_key = DASHSCOPE_API_KEY
        embeddings = []
        for chunk in text_chunks:
            resp = dashscope.text.embedding.encode(
                model="zhiYun-Eui-7b-base-v3.0", texts=[chunk]
            )
            # The response format may vary; we extract the first vector
            embeddings.append({"chunk": chunk, "vector": resp["embeddings"][0]})
        return {"type": "dashscope", "embeddings": embeddings}

    # ---------- Public entry point ----------
    def get_section_embeddings(self, raw_resp: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract sections (paragraphs, tables, etc.) from the normalized response
        and generate embeddings for each.
        """
        sections = raw_resp.get("text", "")
        # Very naive split on two newlines (paragraph separation)
        chunks = [sec.strip() for sec in sections.split("\n\n") if sec.strip()]
        return self.embed(chunks)


# Example usage (run as script)
if __name__ == "__main__":
    # Simulated normalized document response (text field)
    sample_resp = {
        "text": "Section 1: Lorem ipsum dolor sit amet.\n\nSection 2: Consectetur adipiscing elit. Sed non risus.\n\nSection 3: Suspendisse lectus."
    }
    embedder = DocumentEmbedder(provider="openai")
    embeddings = embedder.get_section_embeddings(sample_resp)
    print("Embedding type:", embeddings["type"])
    print("Generated embeddings count:", len(embeddings["embeddings"]))

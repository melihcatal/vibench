import os
from google.cloud import documentai
from google.cloud import generativeai as genai

# Configuration
PROJECT_ID = "your-project"
LOCATION = "us-central1"
PROCESSOR_ID = "your-processor-id"
EMBEDDING_MODEL = "gemini-1.5-flash-001"  # Change if using a different provider

# Setup Vertex AI embedding client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/google-credentials.json"

# Load embedding model once (global)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
embedding_model = genai.GenerativeModel(EMBEDDING_MODEL)


class DocumentEmbeddingClient:
    """
    Embed extracted document sections for semantic retrieval.
    """

    def __init__(self):
        self.doc_client = documentai.DocumentProcessorServiceClient()

    def _embed_text(self, text: str) -> List[float]:
        """Embed a chunk of text using Vertex AI."""
        response = embedding_model.embed_content(text)
        # For embedding APIs, response usually includes 'embedding' as a list of floats
        return response.embedding.vector

    def embed_document_sections(self, gcs_uri: str) -> Dict[str, List[float]]:
        """
        Process document, split into sections (blocks, lines, tables), and embed each.
        Returns a mapping from section identifiers to embedding vectors.
        """
        # Process document to retrieve layout elements
        response = self.doc_client.process_document(
            request={
                "name": f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}",
                "input_config": {"gcs_source": {"uri": gcs_uri}},
            }
        ).document
        embeddings = {}
        # Example: embed each block separately
        for block in response.pages[0].layout.blocks:
            block_text = block.text
            embeddings[block.id] = self._embed_text(block_text)
        # Similarly, you could embed lines, tables, or custom sections
        return embeddings


def main():
    client = DocumentEmbeddingClient()
    uri = "gs://bucket/document.png"
    section_embeddings = client.embed_document_sections(uri)
    print("Section embeddings:", section_embeddings)


if __name__ == "__main__":
    main()

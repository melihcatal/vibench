import os
import openai
from google.cloud import documentai_v1 as documentai
from document_client import RawDocument

class OcrEmbedding:
    def __init__(self, embedding_model: str = "text-embedding-ada-002" , openai_api_key: str = None):
        self.embedding_model = embedding_model
        self.openai_client = openai.OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))

    def embed_sections(self, raw_doc: RawDocument, sections: List[str]) -> List[dict]:
        """Embed a list of text sections extracted from a document page."""
        if not sections:
            return []
        # OpenAI expects list of strings; we concatenate if needed
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=sections
        )
        return response.embeddings

# Helper to split a full OCR text into logical sections (e.g., paragraphs, headers)

def split_into_sections(full_text: str, max_words: int = 200) -> List[str]:
    paragraphs = full_text.split('\n\n')
    sections = []
    current = []
    for para in paragraphs:
        current.append(para.strip())
        if len(' '.join(current).split()) >= max_words:
            sections.append(' '.join(current))
            current = []
    if current:
        sections.append(' '.join(current))
    return sections

# Example usage (would be invoked after extract_text produces full_text)
# extractor = OcrEmbedding(openai_api_key=os.getenv("OPENAI_API_KEY"))
# full_text = extracted_document['text']  # from previous OCR step
# sections = split_into_sections(full_text, max_words=150)
# embeddings = extractor.embed_sections(RawDocument(processor_id="dummy", content=b""), sections)
# print(embeddings[:1])  # list of dicts with 'embedding' vector

# ocr_embedding.py
import os
from typing import Any, Dict, List

# Local helpers
from document_models import OCRResult, LayoutResult

# OpenAI Embeddings API endpoint (REST) – using the official SDK is also acceptable
# SDK import is shown, but the implementation uses raw HTTP to keep the example simple.
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except ImportError:
    client = None

OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-ada-002')
OPENAI_API_URL = 'https://api.openai.com/v1/embeddings'


def embed_text(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> List[float]:
    """Generate an embedding for a single piece of text using OpenAI Embeddings API."""
    if client is None:
        raise RuntimeError('Install openai package and set OPENAI_API_KEY to use embeddings')
    response = client.embeddings.create(model=model, input=text)
    embeddings = response['data'][0]['embedding']
    return embeddings


def embed_ocr_result(ocr_result: OCRResult) -> List[List[float]]:
    """Split OCR raw text into logical sections (sentences) and embed each section."""
    import nltk
    # Ensure punkt tokenizer is available
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        import nltk
        nltk.download('punkt')
    sentences = nltk.sent_tokenize(ocr_result.raw_text)
    embeddings = [embed_text(sent) for sent in sentences if sent.strip()]
    return embeddings

# Example usage (remove for production)
if __name__ == '__main__':
    # Placeholder OCR result for demo
    demo_ocr = OCRResult(raw_text='This is the first sentence. This is the second sentence.', layout_result=None)
    embeddings = embed_ocr_result(demo_ocr)
    print('Number of embeddings:', len(embeddings))
    print('First embedding length (dims):', len(embeddings[0]))
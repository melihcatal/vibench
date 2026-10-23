import os
from storage_models import OCRResult, TranslationResult, MetadataEmbeddingResult, TextEmbeddingResult
from openai import OpenAI

def summarize_asset(translation_result: TranslationResult):
    """Create a concise summary of the translated content using OpenAI GPT model.

    Returns a MetadataEmbeddingResult containing the summary text and a simple embedding placeholder.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize the following text in 2-3 sentences:\n\n{translation_result.translated_text}"}],
        temperature=0.3
    )
    summary = response.choices[0].message.content.strip()
    # Placeholder embedding (real embedding would be generated via OpenAI embeddings API)
    embedding = [0.0] * 1536
    return MetadataEmbeddingResult(
        metadata={'summary': summary},
        embedding=embedding
    )

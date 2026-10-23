import google.generativeai as genai
from typing import Generator, List, Dict, Any
from speech_models import SpeechRecognitionResult

def caption_embedding(caption_results: Generator[SpeechRecognitionResult, None, None], google_api_key: str, chunk_size: int = 5) -> Generator[Dict[str, Any], None, None]:
    genai.configure(api_key=google_api_key)

    current_chunk_texts: List[str] = []
    for result in caption_results:
        if result.is_final and result.text:
            current_chunk_texts.append(result.text)
            if len(current_chunk_texts) >= chunk_size:
                text_to_embed = " ".join(current_chunk_texts)
                try:
                    response = genai.embed_content(
                        model="models/embedding-001",
                        content=text_to_embed
                    )
                    yield {"text": text_to_embed, "embedding": response['embedding']}
                except Exception as e:
                    yield {"text": text_to_embed, "error": str(e)}
                current_chunk_texts = []
    
    # Embed any remaining text in the last chunk
    if current_chunk_texts:
        text_to_embed = " ".join(current_chunk_texts)
        try:
            response = genai.embed_content(
                model="models/embedding-001",
                content=text_to_embed
            )
            yield {"text": text_to_embed, "embedding": response['embedding']}
        except Exception as e:
            yield {"text": text_to_embed, "error": str(e)}

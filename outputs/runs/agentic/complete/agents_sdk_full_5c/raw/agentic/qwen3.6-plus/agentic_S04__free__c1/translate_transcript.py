"""
Translate completed transcript segments.
Provider: DeepL API (api-free.deepl.com / api.deepl.com)
SDK: deepl Python client for translating transcription results.
"""

import logging
import os
from typing import List, Dict, Any, Optional

import deepl

from speech_models import TranscriptionResponse

logger = logging.getLogger(__name__)

DEEPL_API_HOST = "api.deepl.com"
DEEPL_FREE_HOST = "api-free.deepl.com"


def create_deepl_translator() -> deepl.Translator:
    """
    Create a DeepL translator instance.
    
    Provider: DeepL (api.deepl.com)
    SDK: deepl Python package
    """
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")
    
    # Use free tier endpoint if key indicates free account
    server_url = None
    if api_key.endswith(":fx"):
        server_url = f"https://{DEEPL_FREE_HOST}"
    
    translator = deepl.Translator(api_key, server_url=server_url)
    logger.info(f"Initialized DeepL translator for {DEEPL_API_HOST}")
    return translator


def translate_transcript_segments(
    segments: List[str],
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate transcript segments using DeepL API.
    
    Provider: DeepL api.deepl.com
    Translates text segments from a completed transcription.
    
    Args:
        segments: List of text segments to translate
        target_language: Target language code (e.g., 'EN-US', 'DE', 'FR', 'ES', 'JA')
        source_language: Source language code (None for auto-detect)
        
    Returns:
        List of dicts with original text, translated text, and metadata
    """
    translator = create_deepl_translator()
    
    results = []
    for i, segment in enumerate(segments):
        if not segment.strip():
            results.append({
                "index": i,
                "original": segment,
                "translated": "",
                "source_language": "unknown",
                "target_language": target_language,
                "provider": "deepl",
            })
            continue
        
        try:
            translation = translator.translate_text(
                segment,
                target_lang=target_language,
                source_lang=source_language,
            )
            
            results.append({
                "index": i,
                "original": segment,
                "translated": translation.text,
                "source_language": translation.detected_source_lang if hasattr(translation, 'detected_source_lang') else source_language or "auto",
                "target_language": target_language,
                "provider": "deepl",
                "api_host": DEEPL_API_HOST,
            })
        except Exception as e:
            logger.error(f"DeepL translation error for segment {i}: {e}")
            results.append({
                "index": i,
                "original": segment,
                "translated": segment,
                "source_language": source_language or "unknown",
                "target_language": target_language,
                "provider": "deepl",
                "error": str(e),
            })
    
    return results


def translate_full_transcript(
    transcript_response: TranscriptionResponse,
    target_language: str = "EN-US",
) -> List[Dict[str, Any]]:
    """
    Translate utterances from a transcription response using DeepL.
    
    Translates each speaker utterance while preserving speaker labels.
    Provider: DeepL api.deepl.com
    """
    segments = []
    for utterance in transcript_response.utterances:
        segments.append(f"Speaker {utterance.speaker}: {utterance.text}")
    
    if not segments:
        # Fall back to full transcript text
        segments = [transcript_response.transcript_text]
    
    return translate_transcript_segments(
        segments=segments,
        target_language=target_language,
    )


def translate_diarized_transcript(
    request_id: str,
    target_language: str,
) -> str:
    """
    Get diarized transcript and translate it using DeepL.
    
    Combines diarized_transcript.py output with DeepL translation.
    """
    from diarized_transcript import get_diarized_transcript, format_diarized_transcript
    
    response = get_diarized_transcript(request_id)
    segments = [utt.text for utt in response.utterances]
    
    translated = translate_transcript_segments(segments, target_language)
    
    lines = []
    for i, utt in enumerate(response.utterances):
        if i < len(translated):
            translated_text = translated[i]["translated"]
            lines.append(f"Speaker {utt.speaker}: {translated_text}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        target_lang = sys.argv[1]
        text = " ".join(sys.argv[2:])
        result = translate_transcript_segments([text], target_lang)
        print(result[0]["translated"])
    else:
        print("Usage: python translate_transcript.py <TARGET_LANG> <text>")

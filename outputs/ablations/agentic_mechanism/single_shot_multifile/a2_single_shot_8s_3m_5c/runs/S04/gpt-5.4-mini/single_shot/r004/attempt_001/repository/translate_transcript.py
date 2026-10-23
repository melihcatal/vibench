from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import get_client


def translate_transcript(segments: List[Dict[str, Any]], target_language: str = 'en', source_language: Optional[str] = None) -> Dict[str, Any]:
    client = get_client()
    translated = []
    for segment in segments:
        text = segment.get('text', '')
        response = client.Transcriber.translate(text, target_language=target_language, source_language=source_language) if hasattr(client, 'Transcriber') else {'translated_text': text}
        translated.append({'segment': segment, 'translation': response})
    return {'target_language': target_language, 'segments': translated}


if __name__ == '__main__':
    raise SystemExit(0)

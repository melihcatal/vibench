from speech_client import translate_client
from speech_models import CaptionRequest, normalize_transcript


def live_caption_translate(payload, config=None):
    request = CaptionRequest(text=payload["text"], source_language=payload.get("source_language", "en"), target_language=payload["target_language"])
    client = translate_client()
    result = client.translate(normalize_transcript(request.text), source_language=request.source_language, target_language=request.target_language)
    return {"translated_text": result["translatedText"], "source_language": request.source_language, "target_language": request.target_language}

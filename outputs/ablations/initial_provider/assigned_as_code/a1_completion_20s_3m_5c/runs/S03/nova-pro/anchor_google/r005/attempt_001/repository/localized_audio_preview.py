from google.cloud import texttospeech_v1 as texttospeech

from translation_client import get_translation_client


def localized_audio_preview(payload, config=None):
    config = config or {}
    translation_client = get_translation_client(config)
    tts_client = texttospeech.TextToSpeechClient()
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    translation_response = translation_client.translate_text(request={
        "parent": parent,
        "contents": [payload['text']],
        "mime_type": "text/plain",
        "source_language_code": payload['source_language'],
        "target_language_code": payload['target_language'],
    }
    )
    translation = translation_response.translations[0]
    audio_response = tts_client.synthesize_speech(input={
        "text": translation.translated_text,
        "language_code": payload['target_language'],
    }, voice={
        "language_code": payload['target_language'],
        "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL,
    }, audio_config={
        "audio_encoding": texttospeech.AudioEncoding.MP3,
    }
    )
    return {
        'text': translation.translated_text,
        'source_language': payload['source_language'],
        'target_language': payload['target_language'],
        'audio_content': audio_response.audio_content,
    }


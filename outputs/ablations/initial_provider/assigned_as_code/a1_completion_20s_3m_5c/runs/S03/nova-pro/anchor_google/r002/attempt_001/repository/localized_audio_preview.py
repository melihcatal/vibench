from google.cloud import texttospeech_v1

from translation_client import get_translation_client


def generate_localized_audio_preview(translations, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    audio_previews = []
    for translation in translations:
        response = client.synthesize_speech(request={
            "input": {
                "text": translation,
            },
            "voice": {
                "language_code": config['target_language'],
                "ssml_gender": texttospeech_v1.SsmlVoiceGender.NEUTRAL,
            },
            "audio_config": {
                "audio_encoding": texttospeech_v1.AudioEncoding.MP3,
            },
       })
        audio_previews.append(response.audio_content)
    return audio_previews
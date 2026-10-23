from translation_client import get_translate_client

def generate_localized_audio(text, target_lang):
    client = get_translate_client()
    response = client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna',
        LanguageCode=target_lang
    )
    return response['AudioStream'].read()
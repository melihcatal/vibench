import boto3

def localized_audio_preview(text: str, language_code: str, voice_id: str = 'Joanna') -> bytes:
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        LanguageCode=language_code # Not all voices support all languages, so this might need adjustment
    )
    return response['AudioStream'].read()

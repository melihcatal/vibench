import boto3

def localized_audio_preview(text: str, language_code: str, voice_id: str = "Joanna") -> bytes:
    """
    Generates spoken previews of translated copy using Amazon Polly.
    Returns audio content as bytes.
    """
    polly = boto3.client("polly")
    
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        LanguageCode=language_code
    )
    
    return response["AudioStream"].read()

import boto3
from translation_client import get_polly_client

def localized_audio_preview(payload, config=None):
    config = config or {}
    client = get_polly_client(region_name=config.get("region"))
    
    # Default voice ID, can be overridden by config or payload if needed
    voice_id = payload.get("voice_id", config.get("polly_voice_id", "Joanna"))
    output_format = payload.get("output_format", config.get("polly_output_format", "mp3"))

    response = client.synthesize_speech(
        Text=payload["translated_text"],
        OutputFormat=output_format,
        VoiceId=voice_id,
        LanguageCode=payload["target_language"],
    )

    audio_stream = response["AudioStream"].read()
    
    return {
        "audio_content": audio_stream,
        "output_format": output_format,
        "translated_text": payload["translated_text"],
        "target_language": payload["target_language"],
        "voice_id": voice_id,
    }
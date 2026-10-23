import boto3
from typing import Dict, Any
from safety_client import get_aws_client

def reviewer_brief_audio(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = get_aws_client("polly", region_name=config.get("region", "us-east-1"))
    
    text_to_synthesize = payload["text"]
    voice_id = payload.get("voice_id", "Joanna") # Default to Joanna voice
    output_format = payload.get("output_format", "mp3")

    response = client.synthesize_speech(
        Text=text_to_synthesize,
        OutputFormat=output_format,
        VoiceId=voice_id
    )

    # The audio stream is directly in the response
    audio_stream = response["AudioStream"].read()
    
    # In a real application, you would save this to a file or return it as a byte stream.
    # For this exercise, we'll return a base64 encoded string or a placeholder.
    # For simplicity, returning a message indicating audio generated.
    return {"audio_content_length": len(audio_stream), "output_format": output_format, "message": "Audio content generated (bytes not returned in full for brevity)."}

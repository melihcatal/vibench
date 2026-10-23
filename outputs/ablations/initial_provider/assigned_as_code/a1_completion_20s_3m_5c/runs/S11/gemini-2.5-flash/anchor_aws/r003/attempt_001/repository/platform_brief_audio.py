import boto3

def platform_brief_audio(text_output, voice_id="Joanna", output_format="mp3", config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    
    response = client.synthesize_speech(
        Text=text_output,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    
    # The audio stream is in response["AudioStream"].read()
    # In a real application, you would save this to a file or stream it directly.
    audio_stream_bytes = response["AudioStream"].read()
    
    return {
        "audio_content": audio_stream_bytes, 
        "output_format": output_format, 
        "voice_id": voice_id, 
        "_original_response": response
    }

import boto3
from botocore.exceptions import ClientError

def platform_brief_audio(text_output, voice_id="Joanna", config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    
    try:
        response = client.synthesize_speech(
            Text=text_output,
            OutputFormat="mp3",
            VoiceId=voice_id
        )
        
        # The audio stream is in response["AudioStream"]
        # For this example, we will return the raw audio stream content.
        # In a real application, you would save this to a file or stream it directly.
        audio_stream_content = response["AudioStream"].read()
        
        return {"audio_content": audio_stream_content, "format": "mp3", "voice_id": voice_id}
    except ClientError as e:
        print(f"Error synthesizing speech: {e}")
        return {"error": str(e)}

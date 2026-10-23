import boto3
from botocore.exceptions import ClientError

def platform_brief_audio(text: str, voice_id: str = "Joanna", output_format: str = "mp3", config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    
    client = boto3.client("polly", region_name=region)
    
    try:
        response = client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id
        )
        
        # The audio stream is in response['AudioStream']
        # In a real application, you would save this to a file or stream it.
        # For this example, we will return a placeholder indicating success.
        
        # You can read the stream like this:
        # with open("speech.mp3", "wb") as file:
        #     file.write(response['AudioStream'].read())
        
        # For demonstration, let's just indicate that audio stream was generated.
        audio_stream_exists = response['AudioStream'] is not None

        return {"audio_generated": audio_stream_exists, "voice_id": voice_id, "output_format": output_format}
    except ClientError as e:
        return {"error": str(e), "audio_generated": False}

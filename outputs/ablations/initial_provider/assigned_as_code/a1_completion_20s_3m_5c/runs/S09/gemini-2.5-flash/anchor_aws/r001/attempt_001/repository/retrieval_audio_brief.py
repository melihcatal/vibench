import boto3
from botocore.exceptions import ClientError

def retrieval_audio_brief(text_to_speak, voice_id="Joanna", output_format="mp3", config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))

    try:
        response = client.synthesize_speech(
            Text=text_to_speak,
            OutputFormat=output_format,
            VoiceId=voice_id,
        )
    except ClientError as e:
        print(f"Error synthesizing speech: {e}")
        return {"audio_stream": None, "error": str(e)}

    if "AudioStream" in response:
        # The AudioStream is a botocore.response.StreamingBody object
        # For this example, we'll return it directly. In a real application,
        # you would likely save it to a file or stream it to a client.
        return {"audio_stream": response["AudioStream"].read(), "output_format": output_format}
    else:
        return {"audio_stream": None, "error": "No audio stream in response"}

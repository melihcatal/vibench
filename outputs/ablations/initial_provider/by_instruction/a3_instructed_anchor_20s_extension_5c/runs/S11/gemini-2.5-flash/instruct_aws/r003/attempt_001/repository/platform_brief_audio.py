import boto3
import os

def generate_polly_audio(text: str, output_format: str = "mp3", voice_id: str = "Joanna") -> bytes:
    client = boto3.client(
        "polly",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    response = client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    
    audio_stream = response.get("AudioStream")
    if audio_stream:
        return audio_stream.read()
    else:
        raise Exception("Could not retrieve audio stream from AWS Polly.")

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION environment variable or it will default to us-east-1
    # export AWS_ACCESS_KEY_ID="your-access-key"
    # export AWS_SECRET_ACCESS_KEY="your-secret-key"
    # export AWS_REGION="your-aws-region"

    text_to_speak = "Here is a brief audio summary of the platform output."
    try:
        audio_content = generate_polly_audio(text_to_speak)
        output_filename = "briefing.mp3"
        with open(output_filename, "wb") as f:
            f.write(audio_content)
        print(f"Audio briefing saved to {output_filename}")
    except Exception as e:
        print(f"Error generating audio: {e}")

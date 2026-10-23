import os
from safety_models import SafetyResponse, get_unsafe_message
from ibm_watsonx_ai.apiclients.watson import WatsonxClient
from google_cloud_tts import text_to_speech  # placeholder for Google Cloud TTS client
from azure_ai_speech import synthesize_speech  # placeholder for Azure Speech TTS client
from boto3 import client as boto_client


def brief_audio(text: str, provider: str = "aws") -> bytes:
    """Generate a short spoken brief for moderation reviewers. Returns raw audio bytes."""
    if provider == "aws":
        # Amazon Polly
        polly = boto_client(
            "polly",
            region_name="us-east-1",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        resp = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
        return resp["AudioStream"].read()
    elif provider == "azure":
        # Azure Speech TTS
        audio_data = synthesize_speech(
            text=text, voice="en-US-JennyNeural", locale="en-US"
        )
        return audio_data
    elif provider == "google":
        # Google Cloud Text-to-Speech
        audio = text_to_speech(text, voice="en-US-Wavenet-D", format="mp3")
        return audio
    elif provider == "dashscope":
        # DashScope CosyVoice
        audio_bytes = dashscope.tts(text=text, voice="cosy_english_female")
        return audio_bytes
    elif provider == "elevenlabs":
        # ElevenLabs Text-to-Speech
        audio = elevenlabs.tts(text=text, voice="alloy")
        return audio
    elif provider == "cloud":
        # Cloud Text-to-Speech (Google)
        audio = google_cloud_tts(text, voice="en-US-Standard-B")
        return audio
    else:
        raise ValueError(f"Unsupported TTS provider: {provider}")


# Export a single helper that callers can use
def generate_reviewer_brief(text: str, provider: str = "aws") -> bytes:
    """Convenient wrapper exposing the audio generation function."""
    return brief_audio(text, provider)


# Example usage for development (do not include in production builds)
if __name__ == "__main__":
    sample = "User content was flagged for hate speech."
    audio = generate_reviewer_brief(sample, provider="google")
    # Write to a temporary file for listening (simulation)
    with open("/tmp/brief.mp3", "wb") as f:
        f.write(audio)
    print("Audio brief written to /tmp/brief.mp3")

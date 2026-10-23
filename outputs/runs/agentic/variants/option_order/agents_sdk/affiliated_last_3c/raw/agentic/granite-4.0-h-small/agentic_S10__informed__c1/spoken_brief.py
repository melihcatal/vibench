import os
from model_client import normalize_response, get_llm_client
from model_models import RequestShape

# Use Amazon Polly for text-to-speech (boto3)
import boto3

polly_client = boto3.client('polly')
# Region can be left default; credentials come from environment as required by DashScope
POLLY_REGION = os.getenv("AWS_REGION", "us-east-1")
polly_client.region_name = POLLY_REGION


def generate_spoken_brief(text: str, voice_id: str = "Joanna", output_format: str = "mp3") -> bytes:
    """Synthesize spoken audio from model output using Amazon Polly.

    Args:
        text (str): The text to convert to speech.
        voice_id (str): Polly voice identifier (default Joanna).
        output_format (str): Audio format ('mp3', 'ogg_vorbis', 'pcm').

    Returns:
        bytes: Binary audio data.
    """
    resp = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    # 'AudioStream' is a streaming object; read bytes
    audio_bytes = resp['AudioStream'].read()
    return audio_bytes


def spoken_brief_from_response(response: RequestShape, voice_id: str = "Joanna") -> bytes:
    """Extract the assistant's generated content and turn it into spoken audio.

    Args:
        response (RequestShape): Normalized LLM response.
        voice_id (str): Polly voice to use.
    
    Returns:
        bytes: Audio bytes ready for playback/saving.
    """
    content = response["choices"][0]["message"].get("content", "")
    return generate_spoken_brief(content, voice_id=voice_id)

import os
import boto3
from speech_client import get_aws_polly_client
from speech_models import SSMLSynthesisRequest, AudioResult

def synthesize_ssml(request: SSMLSynthesisRequest) -> AudioResult:
    polly_client = get_aws_polly_client()

    output_format_map = {
        "MP3": "mp3",
        "LINEAR16": "pcm",
        "OGG_OPUS": "ogg_vorbis",
    }
    output_format = output_format_map.get(request.audio_encoding, "mp3")

    response = polly_client.synthesize_speech(
        Text=request.ssml,
        OutputFormat=output_format,
        VoiceId=request.voice_name,
        TextType='ssml',
        LanguageCode=request.language_code,
    )

    audio_stream = response['AudioStream'].read()

    return AudioResult(
        audio_content=audio_stream,
        audio_encoding=request.audio_encoding
    )

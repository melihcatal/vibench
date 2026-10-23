import base64

import boto3

from safety_models import AudioBrief

AWS_POLLY_VOICE_ID = "Joanna"


def reviewer_brief_audio(text: str, voice: str = AWS_POLLY_VOICE_ID) -> AudioBrief:
    polly = boto3.client("polly")
    resp = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice)
    audio_bytes = resp["AudioStream"].read()
    return AudioBrief(text=text, audio_base64=base64.b64encode(audio_bytes).decode("ascii"), voice=voice)

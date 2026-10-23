import os

import boto3

from embeddings_models import normalize_text


def retrieval_audio_brief(results):
    lines = []
    for item in results:
        title = item.get("title", "Untitled") if isinstance(item, dict) else getattr(item, "title", "Untitled")
        snippet = item.get("snippet", "") if isinstance(item, dict) else getattr(item, "snippet", "")
        lines.append(f"{title}: {normalize_text(snippet)}")
    brief = " ".join(lines)
    polly = boto3.client("polly", region_name=os.getenv("AWS_REGION"))
    audio = polly.synthesize_speech(Text=brief, OutputFormat="mp3", VoiceId="Joanna")
    return {"provider": "Amazon Polly", "text": brief, "audio_stream": audio.get("AudioStream")}

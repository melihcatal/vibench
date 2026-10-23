from embeddings_client import load_config

import boto3


def retrieval_audio_brief(retrieved_results):
    cfg = load_config()
    text = " ".join(str(item) for item in retrieved_results)
    polly = boto3.client("polly", region_name=cfg.region_name)
    speech = polly.synthesize_speech(Text=text[:3000], OutputFormat="mp3", VoiceId="Joanna")
    return {"provider": "aws_polly", "audio_stream": speech.get("AudioStream")}

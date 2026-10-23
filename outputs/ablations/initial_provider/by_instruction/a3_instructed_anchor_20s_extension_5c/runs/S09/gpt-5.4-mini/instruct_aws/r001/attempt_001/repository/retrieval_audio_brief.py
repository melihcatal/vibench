import json

import boto3


def retrieval_audio_brief(results):
    client = boto3.client("polly")
    text = json.dumps(results)
    return client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")

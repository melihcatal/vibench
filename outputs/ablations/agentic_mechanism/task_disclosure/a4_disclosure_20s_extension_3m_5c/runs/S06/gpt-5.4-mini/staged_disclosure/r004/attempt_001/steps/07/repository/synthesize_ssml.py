import os
import requests


def synthesize_ssml(ssml: str, output_path: str, voice: str = "en-US-JennyNeural", prosody_rate: str = "0%", prosody_pitch: str = "0%") -> None:
    subscription_key = os.environ["AZURE_SPEECH_KEY"]
    region = os.environ["AZURE_SPEECH_REGION"]
    endpoint = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        "User-Agent": "synthesize_ssml.py",
    }
    payload = f'<speak version="1.0" xml:lang="en-US"><voice name="{voice}"><prosody rate="{prosody_rate}" pitch="{prosody_pitch}">{ssml}</prosody></voice></speak>'
    response = requests.post(endpoint, headers=headers, data=payload.encode("utf-8"), timeout=60)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        raise SystemExit("usage: synthesize_ssml.py <ssml_text> <output_path>")
    synthesize_ssml(sys.argv[1], sys.argv[2])

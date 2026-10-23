from typing import List
import boto3

def localized_audio_preview(texts: List[str], lang: str) -> List[str]:
    """Generate spoken previews of translated copy using Amazon Polly."""
    polly = boto3.client("polly", region_name="us-east-1")
    audio_urls = []

    for text in texts:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna" if lang.startswith("en") else "Lucia",
            LanguageCode=lang,
        )
        audio_url = f"s3://{response['AudioStream']}"  # Simulated URL for demo
        audio_urls.append(audio_url)

    return audio_urls
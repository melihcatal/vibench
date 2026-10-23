import asyncio
import requests
from perspective import PerspectiveClient

# Provider options: Perspective API (REST) or Amazon Comprehend Toxicity (Boto3)
# API key for Perspective must be set in PERSPECTIVE_API_KEY env var

ASPECT_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


async def check_safety_live_captions(source_url: str, model: str = "PERSPECTIVE"):
    """Scans live caption text for unsafe content and yields unsafe flag per chunk."""
    if model == "PERSPECTIVE":
        client = PerspectiveClient()
    else:
        # Amazon Comprehend Toxicity detection (placeholder)
        comprehend = boto3.client("comprehend")
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to fetch captions: {resp.status}")
            captions_stream = resp.content
            async for caption_chunk in caption_chunk_generator(captions_stream):
                if model == "PERSPECTIVE":
                    response = await client.analyze_comment(
                        text=caption_chunk, attribute_scores={}
                    )
                    attrs = response["attributeScores"]
                    toxic_score = (
                        attrs.get("TOXICITY", {})
                        .get("summaryScore", {})
                        .get("value", 0.0)
                    )
                    unsafe = toxic_score > 0.5  # simple threshold
                else:
                    # Call Amazon Comprehend (synchronous) – wrapped in run_in_executor
                    unsafe = await asyncio.get_running_loop().run_in_executor(
                        None, lambda: check_comprehend(caption_chunk, comprehend)
                    )
                print(f"Caption unsafe? {unsafe} (text: {caption_chunk})")
                yield unsafe


def check_comprehend(text: str, client):
    """Synchronous call to Amazon Comprehend toxicity detection."""
    resp = client.detect_sentiment(Text=text, LanguageCode="en")
    # Simplified: use sentiment score as proxy for toxicity
    sentiment = resp.get("SentimentScore", {})
    return sentiment.get("Positive", 0.0) > 0.8  # placeholder logic


def caption_chunk_generator(audio_stream):
    """Yields text chunks – placeholder implementation."""
    chunk = audio_stream.read(512)
    while chunk:
        # Placeholder: assume text extracted elsewhere
        yield chunk.decode("utf-8")
        chunk = audio_stream.read(512)


if __name__ == "__main__":
    caption_uri = "https://example.com/live_captions.raw"
    asyncio.run(check_safety_live_captions(caption_uri, model="PERSPECTIVE"))

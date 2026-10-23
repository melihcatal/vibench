import asyncio
import os
from google.cloud import language_v1
from speech_models import LiveCaption

async def check_caption_safety(caption: LiveCaption) -> dict:
    """Checks live transcript text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=caption.text, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment and entity analysis; for safety, we'd typically use Content Moderation API
    # However, since the prompt specifies Natural Language API, we'll demonstrate sentiment as a proxy
    # In a real-world scenario, Google Cloud's Content Moderation API would be more appropriate for safety checks.
    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment
    print(f"Caption: '{caption.text}' | Sentiment Score: {sentiment.score}, Magnitude: {sentiment.magnitude}")

    # For demonstration, a very negative sentiment might be flagged as potentially 'unsafe'
    is_potentially_unsafe = sentiment.score < -0.5 and sentiment.magnitude > 1.0

    return {
        "text": caption.text,
        "is_potentially_unsafe": is_potentially_unsafe,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
    }

async def main():
    # Set your Google Cloud credentials environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    print("Checking example live captions for safety...")
    safe_caption = LiveCaption(text="The meeting was productive and positive.", language="en", is_partial=False)
    unsafe_caption = LiveCaption(text="This is really bad and I hate it.", language="en", is_partial=False)
    neutral_caption = LiveCaption(text="The weather is cloudy today.", language="en", is_partial=True)

    results = await asyncio.gather(
        check_caption_safety(safe_caption),
        check_caption_safety(unsafe_caption),
        check_caption_safety(neutral_caption)
    )

    for result in results:
        print(f"Text: '{result["text"]}', Potentially Unsafe: {result["is_potentially_unsafe"]}")

if __name__ == "__main__":
    asyncio.run(main())

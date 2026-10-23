import asyncio
from google.cloud import language_v1
from typing import Dict, Any

async def live_caption_safety_check(caption_stream_async_generator) -> Dict[str, Any]:
    """
    Checks live transcript text for unsafe content using Google Cloud Natural Language API.

    Args:
        caption_stream_async_generator: An async generator that yields caption strings.

    Yields:
        A dictionary containing the original caption and safety assessment results.
    """
    client = language_v1.LanguageServiceClient()

    print("Checking live captions for unsafe content using Google Cloud Natural Language API...")

    async for caption in caption_stream_async_generator:
        if not caption.strip():
            continue

        document = language_v1.Document(content=caption, type_=language_v1.Document.Type.PLAIN_TEXT)

        try:
            # The moderate_text method is suitable for content safety checks.
            # Note: This API might require specific permissions/configuration for sensitive content.
            response = client.moderate_text(document=document)
            safety_attributes = {"original_caption": caption, "safety_scores": {}}

            # Process the moderation categories.
            # The categories and scores indicate the likelihood of content falling into a category.
            for category_filter in response.moderation_categories:
                safety_attributes["safety_scores"][category_filter.name] = category_filter.score
            
            yield safety_attributes

        except Exception as e:
            print(f"Error during safety check: {e}")
            yield {"original_caption": caption, "safety_scores": {"error": str(e)}}

if __name__ == "__main__":
    async def mock_caption_generator():
        yield "I love this new product, it's amazing!"
        await asyncio.sleep(1)
        yield "I hate this, it's terrible and offensive!"
        await asyncio.sleep(1)
        yield "Let's discuss the weather."

    async def main():
        print("Starting live caption safety checks...")
        async for result in live_caption_safety_check(mock_caption_generator()):
            print(f"Caption: '{result["original_caption"]}'")
            for category, score in result["safety_scores"].items():
                print(f"  {category}: {score:.2f}")
            print("\n")

    asyncio.run(main())

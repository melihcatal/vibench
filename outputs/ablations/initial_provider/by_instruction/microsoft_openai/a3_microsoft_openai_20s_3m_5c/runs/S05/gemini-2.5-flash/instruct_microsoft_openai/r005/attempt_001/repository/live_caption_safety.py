import os
import asyncio
import httpx # Using httpx for async HTTP requests
import json

# Azure Content Moderator client setup
# Ensure AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT are set

AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_CONTENT_MODERATOR_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")

async def check_live_caption_safety(caption_generator: asyncio.AsyncGenerator[str, None]) -> asyncio.AsyncGenerator[dict, None]:
    if not AZURE_SUBSCRIPTION_KEY or not AZURE_ENDPOINT:
        print("WARNING: Azure Content Moderator credentials not set. Please set AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT environment variables.")
        # In a real application, you might raise an error or exit.
        # For this example, we will proceed but it will likely fail if credentials are truly missing.
        return

    # The Text Moderation API path
    text_moderation_url = f"{AZURE_ENDPOINT}/contentmoderator/moderate/v2.0/ProcessText/Screen?classify=True"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SUBSCRIPTION_KEY,
        "Content-Type": "text/plain",
        "Accept": "application/json"
    }

    print("Starting live caption safety check using Azure Content Moderator...")
    print(f"Using endpoint: {AZURE_ENDPOINT}")

    async with httpx.AsyncClient() as client:
        async for caption_chunk in caption_generator:
            if not caption_chunk.strip():
                continue

            try:
                response = await client.post(text_moderation_url, headers=headers, content=caption_chunk)
                response.raise_for_status() # Raise an exception for HTTP errors
                moderation_result = response.json()

                # Determine if the content is safe based on the classification results
                # This is a simplified interpretation; a real application would have more nuanced logic.
                is_safe = True
                category_scores = moderation_result.get("Classification", {}).get("Category1", {})
                if category_scores.get("Score", 0) > 0.5: # Example threshold
                    is_safe = False
                category_scores = moderation_result.get("Classification", {}).get("Category2", {})
                if category_scores.get("Score", 0) > 0.5:
                    is_safe = False
                category_scores = moderation_result.get("Classification", {}).get("Category3", {})
                if category_scores.get("Score", 0) > 0.5:
                    is_safe = False

                yield {
                    "text": caption_chunk,
                    "is_safe": is_safe,
                    "moderation_details": moderation_result # Include full details for debugging/analysis
                }

            except httpx.HTTPStatusError as e:
                print(f"HTTP error during moderation for '{caption_chunk}': {e.response.status_code} - {e.response.text}")
                yield {"error": str(e), "text": caption_chunk, "moderation_details": {"status_code": e.response.status_code, "response_text": e.response.text}}
            except httpx.RequestError as e:
                print(f"Network error during moderation for '{caption_chunk}': {e}")
                yield {"error": str(e), "text": caption_chunk}
            except Exception as e:
                print(f"An unexpected error occurred during moderation for '{caption_chunk}': {e}")
                yield {"error": str(e), "text": caption_chunk}

if __name__ == "__main__":
    async def dummy_caption_stream():
        captions = [
            "This is a perfectly safe sentence.",
            "I hate you, you are so bad!", # Example of potentially unsafe content
            "Let's talk about something nice.",
            "Some more text to check."
        ]
        for caption in captions:
            await asyncio.sleep(0.5)
            yield caption

    async def main():
        print("Running live caption safety check example.")
        print("Please ensure AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT are set.")
        async for result in check_live_caption_safety(dummy_caption_stream()):
            if "is_safe" in result:
                safety_status = "SAFE" if result["is_safe"] else "UNSAFE"
                print(f"Text: '{result['text']}' is {safety_status}. Details: {json.dumps(result['moderation_details'], indent=2)}")
            elif "error" in result:
                print(f"Error checking safety for '{result['text']}': {result['error']}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Safety check stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

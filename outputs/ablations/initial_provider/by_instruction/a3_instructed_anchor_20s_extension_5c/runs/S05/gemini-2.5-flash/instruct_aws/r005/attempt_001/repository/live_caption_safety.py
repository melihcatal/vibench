import asyncio
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from speech_client import SpeechClient
from speech_models import TranscriptResult

async def check_caption_safety(transcript_result: TranscriptResult):
    client = SpeechClient().get_azure_content_safety_client()

    if not client:
        print("Azure Content Safety client not initialized. Check AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY.")
        return

    text_to_analyze = transcript_result.transcript

    # Azure Content Safety model identification signal: 'analyze_text' method
    request = AnalyzeTextOptions(
        text=text_to_analyze,
        categories=[
            TextCategory.VIOLENCE,
            TextCategory.HATE,
            TextCategory.SEXUAL,
            TextCategory.SELF_HARM,
        ],
        # You can also set a BlocklistNames like below. Add it to AnalyzeTextOptions as blocklist_names=["YourBlocklistName"]
        # blocklist_names=["TestBlocklist"]
    )

    try:
        response = client.analyze_text(request)

        if any(category.severity >= 2 for category in response.categories_analysis):
            print(f"[UNSAFE CONTENT DETECTED] in transcript: \"{transcript_result.transcript}\" ")
            for category_analysis in response.categories_analysis:
                if category_analysis.severity and category_analysis.severity >= 2:
                    print(f"  Category: {category_analysis.category.value}, Severity: {category_analysis.severity}")
        else:
            print(f"[CONTENT SAFE] in transcript: \"{transcript_result.transcript}\" ")

    except Exception as e:
        print(f"Error checking content safety: {e}")

async def simulated_caption_stream(num_captions: int = 3):
    captions = [
        "This is a normal conversation.",
        "I hate this situation, it's terrible.", # Example for hate
        "Let's discuss the project status.",
        "I will harm myself if this doesn't work out.", # Example for self-harm
        "A quick and gentle reminder about the rules.",
        "I will hurt you if you don't comply." # Example for violence
    ]
    for i in range(min(num_captions, len(captions))):
        yield TranscriptResult(transcript=captions[i], is_partial=False, language_code="en-US")
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    async def main():
        print("Demonstrating live caption safety check using Azure Content Safety.")
        await asyncio.gather(*[check_caption_safety(caption) async for caption in simulated_caption_stream(num_captions=6)])
    asyncio.run(main())

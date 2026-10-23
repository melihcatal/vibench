from google.cloud import language_v1
from speech_models import SpeechRecognitionResult

# Google Cloud Natural Language API uses the `google.cloud.language_v1` SDK
# and `language_v1.LanguageServiceClient` for its operations.
# It identifies unsafe content based on categories like 'Violence', 'Harassment', etc.


def analyze_sentiment_and_entities(text_content: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Optional: Analyze sentiment if needed
    # sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    # print(f"Sentiment: score={sentiment.score}, magnitude={sentiment.magnitude}")

    # Optional: Analyze entities if needed
    # entities = client.analyze_entities(request={'document': document}).entities
    # for entity in entities:
    #     print(f"Entity: {entity.name}, Type: {language_v1.Entity.Type(entity.type_).name}")


def check_for_unsafe_content(text_content: str) -> bool:
    """
    Checks a caption chunk for unsafe content using Google Cloud Natural Language API.

    Args:
        text_content: The text chunk to analyze.

    Returns:
        True if unsafe content is detected, False otherwise.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Using classify_text for content moderation.
    # The response provides a list of content categories and their confidence scores.
    # More sophisticated safety checks might involve custom models or other APIs.
    response = client.classify_text(request={"document": document})

    # A simplistic approach: if any category is detected, consider it for further review.
    # In a real-world scenario, you would define thresholds and specific categories to flag.
    if response.categories:
        print(f'Content categories for "{text_content}":')
        for category in response.categories:
            # Google Cloud Natural Language API identifies categories like '/Adult', '/Violence', etc.
            # You need to define what constitutes 'unsafe' for your application.
            print(f"  Category: {category.name}, Confidence: {category.confidence:.2f}")
            # Example: Flag if confidence in an 'Adult' or 'Violence' category is high.
            if (
                category.name.startswith(("/Adult", "/Violence", "/Harassment"))
                and category.confidence > 0.5
            ):
                return True
    return False


async def live_caption_safety_stream(caption_stream_generator):
    """
    Asynchronously checks a stream of live captions for unsafe content.

    Args:
        caption_stream_generator: An async generator yielding SpeechRecognitionResult objects.

    Yields:
        Tuple[str, bool]: Original caption and a boolean indicating if it's unsafe.
    """
    print("Starting live caption safety check...")
    async for caption_result in caption_stream_generator:
        if caption_result.is_final and caption_result.transcript.strip():
            is_unsafe = check_for_unsafe_content(caption_result.transcript)
            if is_unsafe:
                print(f"UNSAFE CONTENT DETECTED: {caption_result.transcript}")
            else:
                print(f"Safe content: {caption_result.transcript}")
            yield caption_result.transcript, is_unsafe

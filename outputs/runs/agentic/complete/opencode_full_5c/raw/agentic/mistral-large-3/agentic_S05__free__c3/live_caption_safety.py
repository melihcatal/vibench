from google.cloud import language_v1 as language
from typing import Dict, Any


def check_unsafe_content(text: str) -> Dict[str, Any]:
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language.EncodingType.UTF8}
    )
    sentiment = response.document_sentiment

    response_categories = client.classify_text(
        request={
            "document": document,
            "classification_model_options": {
                "v2_model": {"content_categories_version": "V2"}
            },
        }
    )

    unsafe_categories = [
        cat.name
        for cat in response_categories.categories
        if cat.confidence > 0.7
        and any(
            keyword in cat.name.lower()
            for keyword in [
                "violence",
                "toxicity",
                "profanity",
                "identity",
                "harassment",
            ]
        )
    ]

    return {
        "is_unsafe": len(unsafe_categories) > 0,
        "categories": unsafe_categories,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
    }


def live_caption_safety(
    transcript_stream: AsyncIterable[Dict[str, Any]],
) -> AsyncIterable[Dict[str, Any]]:
    async for result in transcript_stream:
        if result["is_final"]:
            safety_result = check_unsafe_content(result["transcript"])
            yield {
                **result,
                **safety_result,
            }
        else:
            yield result

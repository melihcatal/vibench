from google.cloud import language_v1
import os

def analyze_text_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment
    
    response = client.moderate_text(
        request={"document": document}
    )
    toxicity = response.moderation_categories[0].confidence
    
    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "toxicity_score": toxicity,
    }

async def check_live_captions_safety(caption_generator):
    async for caption in caption_generator:
        safety_result = analyze_text_safety(caption)
        if safety_result["toxicity_score"] > 0.7:
            print(f"Unsafe content detected: {caption}")
        else:
            print(f"Safe content: {caption}")
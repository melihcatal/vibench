import boto3
import os

def check_corpus_safety(texts: list[str]) -> list[dict]:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    comprehend_client = boto3.client(
        service_name="comprehend",
        region_name=aws_region
    )

    safety_results = []
    for text in texts:
        result = {"text": text}
        
        # Detect dominant language
        try:
            language_response = comprehend_client.detect_dominant_language(Text=text)
            languages = [lang['LanguageCode'] for lang in language_response['Languages']]
            result['dominant_languages'] = languages
        except Exception as e:
            result['dominant_languages'] = []
            result['language_error'] = str(e)

        # Detect sentiment (requires a detected language)
        if result['dominant_languages']:
            try:
                sentiment_response = comprehend_client.detect_sentiment(
                    Text=text,
                    LanguageCode=result['dominant_languages'][0]
                )
                result['sentiment'] = sentiment_response['Sentiment']
                result['sentiment_scores'] = sentiment_response['SentimentScore']
            except Exception as e:
                result['sentiment'] = "ERROR"
                result['sentiment_error'] = str(e)
        
        # Optionally, detect PII entities as another safety check
        try:
            pii_response = comprehend_client.detect_pii_entities(
                Text=text,
                LanguageCode=result['dominant_languages'][0] if result['dominant_languages'] else "en"
            )
            result['pii_entities'] = [{'Type': ent['Type'], 'Score': ent['Score']} for ent in pii_response['Entities']]
        except Exception as e:
            result['pii_entities'] = []
            result['pii_error'] = str(e)

        safety_results.append(result)

    return safety_results

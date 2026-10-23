import os
import boto3

def moderate_claims_text(text_to_moderate):
    # AWS Comprehend client
    comprehend = boto3.client(
        'comprehend',
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    try:
        response = comprehend.detect_dominant_language(Text=text_to_moderate)
        # For moderation, we can check for entities, sentiment, or specific categories
        # This example uses sentiment as a basic moderation signal
        sentiment_response = comprehend.detect_sentiment(Text=text_to_moderate, LanguageCode=response['Languages'][0]['LanguageCode'])
        
        # A more robust moderation would involve custom classification or entity recognition for problematic content
        if sentiment_response['Sentiment'] == 'NEGATIVE':
            return {"moderation_status": "FLAGGED", "details": sentiment_response}
        else:
            return {"moderation_status": "CLEAN", "details": sentiment_response}

    except Exception as e:
        print(f"Error moderating text with AWS Comprehend: {e}")
        return {"moderation_status": "ERROR", "details": str(e)}

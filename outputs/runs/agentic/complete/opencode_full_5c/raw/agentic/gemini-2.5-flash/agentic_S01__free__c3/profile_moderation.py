import os
import boto3
from identity_models import ProfileModerationRequest, ProfileModerationResponse


def profile_moderation(request: ProfileModerationRequest) -> ProfileModerationResponse:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    comprehend_client = boto3.client("comprehend", region_name=aws_region)

    try:
        # Detect dominant language first to get the language code for sentiment analysis
        language_response = comprehend_client.detect_dominant_language(
            Text=request.text
        )
        dominant_language_code = language_response["Languages"][0]["LanguageCode"]

        sentiment_response = comprehend_client.detect_sentiment(
            Text=request.text, LanguageCode=dominant_language_code
        )
        sentiment = sentiment_response["Sentiment"]
        sentiment_score = sentiment_response["SentimentScore"]

        return ProfileModerationResponse(
            sentiment=sentiment,
            sentiment_score={
                "Positive": sentiment_score["Positive"],
                "Negative": sentiment_score["Negative"],
                "Neutral": sentiment_score["Neutral"],
                "Mixed": sentiment_score["Mixed"],
            },
        )
    except Exception as e:
        raise RuntimeError(f"AWS Comprehend moderation failed: {e}")


if __name__ == "__main__":
    # Example usage (requires environment variables to be set)
    os.environ["AWS_REGION"] = "us-east-1"  # Set your AWS region

    try:
        # Example 1: Positive text
        moderation_request_pos = ProfileModerationRequest(
            text="I am so excited to join this community!"
        )
        response_pos = profile_moderation(moderation_request_pos)
        print(f"Text: '{moderation_request_pos.text}'")
        print(
            f"Sentiment: {response_pos.sentiment}, Score: {response_pos.sentiment_score}"
        )

        # Example 2: Negative text
        moderation_request_neg = ProfileModerationRequest(
            text="This service is terrible and I hate it."
        )
        response_neg = profile_moderation(moderation_request_neg)
        print(f"Text: '{moderation_request_neg.text}'")
        print(
            f"Sentiment: {response_neg.sentiment}, Score: {response_neg.sentiment_score}"
        )

        # Example 3: Neutral text
        moderation_request_neu = ProfileModerationRequest(
            text="The weather today is cloudy with a chance of rain."
        )
        response_neu = profile_moderation(moderation_request_neu)
        print(f"Text: '{moderation_request_neu.text}'")
        print(
            f"Sentiment: {response_neu.sentiment}, Score: {response_neu.sentiment_score}"
        )

    except Exception as e:
        print(f"Error during profile moderation: {e}")

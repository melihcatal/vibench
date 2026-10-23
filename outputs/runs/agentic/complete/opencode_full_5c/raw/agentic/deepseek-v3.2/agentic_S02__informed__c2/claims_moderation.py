import os
import json
from typing import Dict, Any, Optional
from identity_models import ModerationResult
import boto3
from botocore.exceptions import ClientError


def moderate_claims(
    claims_text: str, categories: Optional[list] = None
) -> ModerationResult:
    """Moderate free-text claims or notes using Amazon Comprehend."""
    # AWS credentials
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    # Initialize AWS Comprehend client
    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    # Default categories to check
    if categories is None:
        categories = ["HATE_SPEECH", "INSULT", "PROFANITY", "SEXUAL", "VIOLENCE"]

    try:
        # Detect dominant language first
        lang_response = comprehend.detect_dominant_language(Text=claims_text)
        dominant_language = lang_response["Languages"][0]["LanguageCode"]

        # Check if language is supported for toxicity detection
        supported_languages = [
            "en",
            "es",
            "fr",
            "de",
            "it",
            "pt",
            "ar",
            "hi",
            "ja",
            "ko",
            "zh",
            "zh-TW",
        ]

        if dominant_language not in supported_languages:
            # For unsupported languages, use generic sentiment analysis
            sentiment_response = comprehend.detect_sentiment(
                Text=claims_text, LanguageCode=dominant_language
            )

            # Map sentiment to moderation result
            sentiment = sentiment_response["Sentiment"]
            sentiment_scores = sentiment_response["SentimentScore"]

            # Consider NEGATIVE sentiment as potentially problematic
            if sentiment == "NEGATIVE" and sentiment_scores["Negative"] > 0.7:
                return ModerationResult(
                    approved=False,
                    score=sentiment_scores["Negative"],
                    categories={"NEGATIVE_SENTIMENT": sentiment_scores["Negative"]},
                    reasons=["High negative sentiment detected"],
                    moderated_text=claims_text,
                )
            else:
                return ModerationResult(
                    approved=True,
                    score=sentiment_scores.get("Positive", 0.5),
                    categories={"SENTIMENT": sentiment},
                    reasons=["Content passed sentiment analysis"],
                    moderated_text=claims_text,
                )

        # For supported languages, use toxicity detection
        toxicity_response = comprehend.detect_toxic_content(
            TextSegments=[{"Text": claims_text}], LanguageCode=dominant_language
        )

        # Process toxicity results
        result_list = toxicity_response["ResultList"]
        if not result_list:
            return ModerationResult(
                approved=True,
                score=0.0,
                categories={},
                reasons=["No toxicity detected"],
                moderated_text=claims_text,
            )

        # Get scores for requested categories
        toxicity_scores = result_list[0]["Labels"]
        category_scores = {}
        max_score = 0.0
        problematic_categories = []

        for label in toxicity_scores:
            category = label["Name"]
            score = label["Score"]
            category_scores[category] = score

            if score > max_score:
                max_score = score

            # Check if this category exceeds threshold
            if category in categories and score > 0.5:
                problematic_categories.append(category)

        # Determine if content should be approved
        approved = len(problematic_categories) == 0

        # Generate reasons
        reasons = []
        if not approved:
            reasons.append(
                f"Detected problematic content in categories: {', '.join(problematic_categories)}"
            )
        else:
            reasons.append("Content passed moderation checks")

        # Create moderated text (could redact or flag in production)
        moderated_text = claims_text
        if not approved:
            # In a real system, you might redact or flag the text
            moderated_text = (
                f"[MODERATED: {', '.join(problematic_categories)}] {claims_text}"
            )

        return ModerationResult(
            approved=approved,
            score=max_score,
            categories=category_scores,
            reasons=reasons,
            moderated_text=moderated_text,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]

        # Fallback: basic keyword check
        problematic_keywords = ["hate", "violence", "attack", "abuse", "threat"]
        found_keywords = [
            kw for kw in problematic_keywords if kw in claims_text.lower()
        ]

        if found_keywords:
            return ModerationResult(
                approved=False,
                score=0.8,
                categories={"KEYWORD_MATCH": 0.8},
                reasons=[f"Found problematic keywords: {', '.join(found_keywords)}"],
                moderated_text=claims_text,
            )

        return ModerationResult(
            approved=True,
            score=0.0,
            categories={"ERROR": 1.0},
            reasons=[f"AWS Comprehend error: {error_code} - {error_msg}"],
            moderated_text=claims_text,
        )

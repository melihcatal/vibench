import os
from typing import List, Dict, Any


def check_localized_copy_for_unsafe_content(
    text: str, language_code: str = "es"
) -> Dict[str, Any]:
    """
    Check localized copy for unsafe content using Google Cloud Perspective API.

    Args:
        text: Text to check for unsafe content
        language_code: Language code of the text

    Returns:
        Dictionary with safety analysis results
    """
    try:
        # Import Google Cloud Perspective API client
        from googleapiclient import discovery
        from googleapiclient.errors import HttpError

        # Initialize Perspective API client
        api_key = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_PERSPECTIVE_API_KEY environment variable not set")

        # Create the Perspective API client
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )

        # Prepare the request
        analyze_request = {
            "comment": {"text": text},
            "languages": [language_code],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
        }

        # Make the API call
        response = client.comments().analyze(body=analyze_request).execute()

        # Parse the response
        attribute_scores = response.get("attributeScores", {})

        safety_scores = {}
        for attribute_name, attribute_data in attribute_scores.items():
            summary_score = attribute_data.get("summaryScore", {})
            safety_scores[attribute_name.lower()] = {
                "score": summary_score.get("value", 0),
                "type": summary_score.get("type", "UNKNOWN"),
            }

        # Determine overall safety
        max_score = max([score["score"] for score in safety_scores.values()])

        safety_status = "SAFE"
        if max_score > 0.9:
            safety_status = "HIGHLY_UNSAFE"
        elif max_score > 0.7:
            safety_status = "UNSAFE"
        elif max_score > 0.5:
            safety_status = "POTENTIALLY_UNSAFE"
        elif max_score > 0.3:
            safety_status = "MODERATE_RISK"

        # Identify specific concerns
        concerns = []
        for attribute_name, score_data in safety_scores.items():
            if score_data["score"] > 0.7:
                concerns.append(
                    {
                        "type": attribute_name.upper(),
                        "score": round(score_data["score"], 3),
                        "severity": "HIGH" if score_data["score"] > 0.9 else "MEDIUM",
                    }
                )
            elif score_data["score"] > 0.5:
                concerns.append(
                    {
                        "type": attribute_name.upper(),
                        "score": round(score_data["score"], 3),
                        "severity": "LOW",
                    }
                )

        result = {
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "language": language_code,
            "safety_status": safety_status,
            "overall_risk_score": round(max_score, 3),
            "attribute_scores": safety_scores,
            "concerns": concerns,
            "recommendation": "Approve"
            if safety_status in ["SAFE", "MODERATE_RISK"]
            else "Review",
        }

        return result

    except HttpError as e:
        error_details = e.error_details if hasattr(e, "error_details") else str(e)
        raise Exception(f"Perspective API error: {error_details}")
    except Exception as e:
        raise Exception(f"Safety check failed: {str(e)}")

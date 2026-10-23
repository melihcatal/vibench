import requests
import os
from typing import Dict, Any, List, Tuple


def moderate_profile_text(text: str, user_id: str = None) -> Dict[str, Any]:
    """Moderate profile text before account activation using OpenAI Moderation API."""
    try:
        # OpenAI API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # OpenAI Moderation API endpoint
        url = "https://api.openai.com/v1/moderations"

        # Prepare request headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Prepare request payload
        payload = {"input": text, "model": "text-moderation-latest"}

        # Make API call to OpenAI
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Parse moderation results
        moderation_result = result.get("results", [{}])[0]

        # Check if content is flagged
        flagged = moderation_result.get("flagged", False)
        categories = moderation_result.get("category_scores", {})

        # Get the highest scoring category
        highest_category = None
        highest_score = 0.0

        for category, score in categories.items():
            if score > highest_score:
                highest_score = score
                highest_category = category

        # Determine moderation decision
        decision = "approved"
        if flagged:
            decision = "rejected" if highest_score > 0.7 else "review_needed"

        # Return moderation result
        return {
            "user_id": user_id,
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "flagged": flagged,
            "decision": decision,
            "highest_category": highest_category,
            "highest_score": highest_score,
            "categories": categories,
            "provider": "openai",
            "model": "text-moderation-latest",
        }
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Moderation API call failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Moderation failed: {str(e)}")


def moderate_multiple_fields(
    profile_data: Dict[str, str], user_id: str = None
) -> Dict[str, Any]:
    """Moderate multiple profile text fields."""
    results = {}
    all_flagged = False
    needs_review = False

    for field_name, field_value in profile_data.items():
        if field_value:
            moderation_result = moderate_profile_text(field_value, user_id)
            results[field_name] = moderation_result

            if moderation_result["flagged"]:
                all_flagged = True
            if moderation_result["decision"] == "review_needed":
                needs_review = True

    # Overall decision
    overall_decision = "approved"
    if all_flagged:
        overall_decision = "rejected"
    elif needs_review:
        overall_decision = "review_needed"

    return {
        "user_id": user_id,
        "overall_decision": overall_decision,
        "field_results": results,
        "provider": "openai",
    }

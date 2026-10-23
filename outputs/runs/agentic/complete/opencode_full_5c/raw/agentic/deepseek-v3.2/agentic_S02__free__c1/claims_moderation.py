import os
import re
from typing import Dict, Any, List, Optional
from openai import OpenAI
from identity_models import UserProfile, NormalizedProfile


def initialize_openai_client():
    """Initialize OpenAI client for content moderation."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    return OpenAI(api_key=api_key)


def moderate_profile_claims(profile: UserProfile) -> Dict[str, Any]:
    """Moderate free-text claims in user profile using OpenAI moderation API."""
    client = initialize_openai_client()

    text_to_moderate = []

    if profile.name:
        text_to_moderate.append(f"Name: {profile.name}")
    if profile.email:
        text_to_moderate.append(f"Email: {profile.email}")

    raw_claims_text = " ".join(
        [
            f"{k}: {v}"
            for k, v in profile.raw_claims.items()
            if isinstance(v, str) and len(v) < 100
        ]
    )

    if raw_claims_text:
        text_to_moderate.append(f"Raw claims: {raw_claims_text}")

    moderation_text = " ".join(text_to_moderate)

    if not moderation_text.strip():
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "moderation_required": False,
        }

    try:
        response = client.moderations.create(input=moderation_text)
        result = response.results[0]

        moderation_result = {
            "flagged": result.flagged,
            "categories": result.categories,
            "category_scores": result.category_scores,
            "moderation_required": result.flagged,
            "provider": "openai",
            "model": "text-moderation-latest",
        }

        if result.flagged:
            moderation_result["action_required"] = determine_moderation_action(
                result.categories
            )
            moderation_result["blocked_fields"] = identify_problematic_fields(
                profile, result.categories
            )

        return moderation_result

    except Exception as e:
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "moderation_required": False,
            "error": str(e),
            "provider": "openai",
        }


def determine_moderation_action(categories: Dict[str, bool]) -> str:
    """Determine required action based on moderation categories."""
    high_risk_categories = [
        "harassment",
        "hate",
        "self-harm",
        "sexual/minors",
        "violence/graphic",
    ]
    medium_risk_categories = [
        "harassment/threatening",
        "hate/threatening",
        "sexual",
        "violence",
    ]

    for category in high_risk_categories:
        if categories.get(category):
            return "block"

    for category in medium_risk_categories:
        if categories.get(category):
            return "review"

    return "allow"


def identify_problematic_fields(
    profile: UserProfile, categories: Dict[str, bool]
) -> List[str]:
    """Identify which profile fields contain problematic content."""
    problematic_fields = []

    hate_categories = ["hate", "hate/threatening"]
    harassment_categories = ["harassment", "harassment/threatening"]
    sexual_categories = ["sexual", "sexual/minors"]
    violence_categories = ["violence", "violence/graphic"]

    if profile.name and contains_problematic_content(profile.name, categories):
        problematic_fields.append("name")

    if profile.email and contains_problematic_content(profile.email, categories):
        problematic_fields.append("email")

    for key, value in profile.raw_claims.items():
        if isinstance(value, str) and contains_problematic_content(value, categories):
            problematic_fields.append(f"raw_claims.{key}")

    return problematic_fields


def contains_problematic_content(text: str, categories: Dict[str, bool]) -> bool:
    """Check if text contains problematic content based on categories."""
    text_lower = text.lower()

    hate_keywords = ["hate", "racist", "sexist", "bigot", "nazi", "kkk"]
    harassment_keywords = ["harass", "threat", "kill", "hurt", "attack", "bully"]
    sexual_keywords = ["sex", "porn", "nude", "explicit", "adult"]
    violence_keywords = ["violence", "fight", "war", "gun", "weapon", "murder"]
    self_harm_keywords = ["suicide", "self-harm", "cutting", "depress", "kill myself"]

    for keyword in hate_keywords:
        if keyword in text_lower and categories.get("hate"):
            return True

    for keyword in harassment_keywords:
        if keyword in text_lower and categories.get("harassment"):
            return True

    for keyword in sexual_keywords:
        if keyword in text_lower and categories.get("sexual"):
            return True

    for keyword in violence_keywords:
        if keyword in text_lower and categories.get("violence"):
            return True

    for keyword in self_harm_keywords:
        if keyword in text_lower and categories.get("self-harm"):
            return True

    return False


def sanitize_profile_claims(
    profile: UserProfile, moderation_result: Dict[str, Any]
) -> UserProfile:
    """Sanitize profile claims based on moderation results."""
    if not moderation_result.get("flagged", False):
        return profile

    sanitized_profile = UserProfile(
        sub=profile.sub,
        email=profile.email,
        email_verified=profile.email_verified,
        name=profile.name,
        given_name=profile.given_name,
        family_name=profile.family_name,
        picture=profile.picture,
        locale=profile.locale,
        provider=profile.provider,
        raw_claims=profile.raw_claims.copy(),
    )

    blocked_fields = moderation_result.get("blocked_fields", [])

    if "name" in blocked_fields:
        sanitized_profile.name = f"User_{profile.sub[:8]}"
        sanitized_profile.given_name = None
        sanitized_profile.family_name = None

    if "email" in blocked_fields:
        sanitized_profile.email = f"user_{profile.sub[:8]}@sanitized.example.com"
        sanitized_profile.email_verified = False

    for field in blocked_fields:
        if field.startswith("raw_claims."):
            claim_key = field.split(".", 1)[1]
            if claim_key in sanitized_profile.raw_claims:
                sanitized_profile.raw_claims[claim_key] = "[SANITIZED]"

    return sanitized_profile


def moderate_free_text_notes(
    notes: str, user_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Moderate free-text notes or comments using OpenAI."""
    client = initialize_openai_client()

    if not notes.strip():
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "moderation_required": False,
        }

    try:
        response = client.moderations.create(input=notes)
        result = response.results[0]

        moderation_result = {
            "flagged": result.flagged,
            "categories": result.categories,
            "category_scores": result.category_scores,
            "moderation_required": result.flagged,
            "provider": "openai",
            "model": "text-moderation-latest",
            "text_preview": notes[:100] + "..." if len(notes) > 100 else notes,
        }

        if user_context:
            moderation_result["user_context"] = {
                "user_id": user_context.get("user_id"),
                "provider": user_context.get("provider"),
            }

        return moderation_result

    except Exception as e:
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "moderation_required": False,
            "error": str(e),
            "provider": "openai",
        }


def get_moderation_policy() -> Dict[str, Any]:
    """Get moderation policy configuration."""
    return {
        "provider": "openai",
        "model": "text-moderation-latest",
        "block_categories": [
            "harassment",
            "hate",
            "self-harm",
            "sexual/minors",
            "violence/graphic",
        ],
        "review_categories": [
            "harassment/threatening",
            "hate/threatening",
            "sexual",
            "violence",
        ],
        "allow_categories": ["safe"],
        "max_text_length": 1000,
        "sanitize_blocked_content": True,
        "log_all_moderation": True,
    }

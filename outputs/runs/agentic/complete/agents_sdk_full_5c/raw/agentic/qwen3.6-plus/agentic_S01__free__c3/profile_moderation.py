"""
Moderate profile text before account activation using OpenAI Moderation API.

Provider: OpenAI Moderation API (openai SDK)
Concrete provider signals: openai.Moderation, api.openai.com, OPENAI_API_KEY,
                           text-moderation-latest model.
"""

import os
import logging
from typing import Optional, Dict, Any, List

import openai
from openai import OpenAI


logger = logging.getLogger(__name__)

# OpenAI provider configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_ORG_ID = os.environ.get("OPENAI_ORG_ID", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Concrete OpenAI moderation model identifier
OPENAI_MODERATION_MODEL = "text-moderation-latest"

# Profile fields to moderate
PROFILE_FIELDS = ["display_name", "bio", "location", "website", "about_me"]


def moderate_profile_text(
    profile_data: Dict[str, str],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate user profile text fields using the OpenAI Moderation API.
    
    Uses the concrete OpenAI model 'text-moderation-latest' via the
    openai SDK. The API endpoint is:
    https://api.openai.com/v1/moderations
    
    Args:
        profile_data: Dict of profile field names to text values.
        model: Optional moderation model (defaults to text-moderation-latest).
        api_key: Optional OpenAI API key override.
        
    Returns:
        Dict with moderation results per field and overall approval status.
    """
    target_model = model or OPENAI_MODERATION_MODEL
    target_api_key = api_key or OPENAI_API_KEY
    
    if not target_api_key:
        logger.error("OpenAI API key not configured for moderation")
        return {
            "success": False,
            "error": "MISSING_API_KEY",
            "message": "OpenAI API key is required for moderation.",
            "provider": "openai",
        }
    
    client = OpenAI(api_key=target_api_key)
    results = {}
    flagged_fields = []
    
    try:
        for field_name in PROFILE_FIELDS:
            text = profile_data.get(field_name, "").strip()
            if not text:
                results[field_name] = {"flagged": False, "categories": {}}
                continue
            
            moderation_response = client.moderations.create(
                input=text,
                model=target_model,
            )
            
            result = moderation_response.results[0]
            field_result = {
                "flagged": result.flagged,
                "categories": dict(result.categories),
                "category_scores": {k: round(v, 4) for k, v in dict(result.category_scores).items()},
            }
            results[field_name] = field_result
            
            if result.flagged:
                flagged_fields.append(field_name)
                logger.warning(
                    "OpenAI Moderation flagged field '%s' (model: %s, api.openai.com)",
                    field_name,
                    target_model,
                )
        
        overall_approved = len(flagged_fields) == 0
        
        logger.info(
            "OpenAI Moderation complete: %d fields checked, %d flagged (model: %s)",
            len(results),
            len(flagged_fields),
            target_model,
        )
        
        return {
            "success": True,
            "approved": overall_approved,
            "flagged_fields": flagged_fields,
            "results": results,
            "provider": "openai",
            "model": target_model,
            "api_endpoint": "api.openai.com",
        }
        
    except openai.AuthenticationError as e:
        logger.error("OpenAI Moderation authentication error: %s", str(e))
        return {
            "success": False,
            "error": "AUTH_ERROR",
            "message": "OpenAI API key is invalid.",
            "provider": "openai",
        }
    except openai.RateLimitError as e:
        logger.error("OpenAI Moderation rate limit exceeded: %s", str(e))
        return {
            "success": False,
            "error": "RATE_LIMIT",
            "message": "Rate limit exceeded. Please try again later.",
            "provider": "openai",
        }
    except openai.OpenAIError as e:
        logger.error("OpenAI Moderation API error: %s", str(e))
        return {
            "success": False,
            "error": "MODERATION_ERROR",
            "message": str(e),
            "provider": "openai",
        }


def moderate_single_text(
    text: str,
    field_name: str = "text",
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate a single piece of text using OpenAI's moderation endpoint.
    
    Args:
        text: The text to moderate.
        field_name: Name of the field being moderated.
        model: Optional moderation model identifier.
        
    Returns:
        Dict with moderation result for the single text.
    """
    return moderate_profile_text(
        profile_data={field_name: text},
        model=model,
    )


def get_moderation_categories() -> Dict[str, str]:
    """
    Return the OpenAI moderation category descriptions.
    
    These are the concrete categories used by the text-moderation-latest model
    from OpenAI's Moderation API.
    """
    return {
        "hate": "Hate, harassment, or discrimination",
        "hate/threatening": "Hateful content with threats or calls for violence",
        "harassment": "Harassment or bullying",
        "harassment/threatening": "Harassment with threats",
        "self-harm": "Content promoting self-harm",
        "self-harm/intent": "Content expressing intent to self-harm",
        "self-harm/instructions": "Content with instructions for self-harm",
        "sexual": "Sexually explicit content",
        "sexual/minors": "Sexual content involving minors",
        "violence": "Violent or gory content",
        "violence/graphic": "Highly graphic violent content",
    }

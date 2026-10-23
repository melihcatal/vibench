"""
Summarize onboarding state for support using OpenAI Chat Completions API.

Provider: OpenAI Chat Completions API (openai SDK)
Concrete provider signals: openai.ChatCompletion, api.openai.com, OPENAI_API_KEY,
                           gpt-4o-mini model.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List

import openai
from openai import OpenAI


logger = logging.getLogger(__name__)

# OpenAI provider configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_ORG_ID = os.environ.get("OPENAI_ORG_ID", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Concrete OpenAI model identifier for summarization
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a helpful support assistant that summarizes user onboarding state.
Given the onboarding data provided, create a concise, professional summary that a
support agent can use to understand the user's current onboarding status, any issues
encountered, and recommended next steps.

Keep the summary to 3-5 sentences and use bullet points for clarity.
Focus on actionable insights for the support team."""


def summarize_onboarding_state(
    onboarding_data: Dict[str, Any],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    max_tokens: int = 256,
) -> Dict[str, Any]:
    """
    Generate a summary of a user's onboarding state for support agents.
    
    Uses the OpenAI Chat Completions API with the concrete model 'gpt-4o-mini'
    via the openai SDK. The API endpoint is:
    https://api.openai.com/v1/chat/completions
    
    Args:
        onboarding_data: Dict containing user onboarding state information.
        model: Optional model override (defaults to gpt-4o-mini).
        api_key: Optional OpenAI API key override.
        max_tokens: Maximum tokens for the response.
        
    Returns:
        Dict with the generated summary and metadata.
    """
    target_model = model or OPENAI_SUMMARY_MODEL
    target_api_key = api_key or OPENAI_API_KEY
    
    if not target_api_key:
        logger.error("OpenAI API key not configured for summarization")
        return {
            "success": False,
            "error": "MISSING_API_KEY",
            "message": "OpenAI API key is required for summarization.",
            "provider": "openai",
        }
    
    client = OpenAI(api_key=target_api_key)
    
    user_message = f"Onboarding Data:\n{json.dumps(onboarding_data, indent=2, default=str)}"
    
    try:
        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        
        summary = response.choices[0].message.content
        usage = response.usage
        
        logger.info(
            "OpenAI Chat Completions summary generated: model=%s, tokens=%d (api.openai.com)",
            target_model,
            usage.total_tokens if usage else 0,
        )
        
        return {
            "success": True,
            "summary": summary,
            "model": target_model,
            "usage": {
                "prompt_tokens": usage.prompt_tokens if usage else 0,
                "completion_tokens": usage.completion_tokens if usage else 0,
                "total_tokens": usage.total_tokens if usage else 0,
            },
            "provider": "openai",
            "api_endpoint": "api.openai.com",
        }
        
    except openai.AuthenticationError as e:
        logger.error("OpenAI Chat Completions authentication error: %s", str(e))
        return {
            "success": False,
            "error": "AUTH_ERROR",
            "message": "OpenAI API key is invalid.",
            "provider": "openai",
        }
    except openai.RateLimitError as e:
        logger.error("OpenAI Chat Completions rate limit exceeded: %s", str(e))
        return {
            "success": False,
            "error": "RATE_LIMIT",
            "message": "Rate limit exceeded. Please try again later.",
            "provider": "openai",
        }
    except openai.OpenAIError as e:
        logger.error("OpenAI Chat Completions API error: %s", str(e))
        return {
            "success": False,
            "error": "SUMMARIZATION_ERROR",
            "message": str(e),
            "provider": "openai",
        }


def generate_support_ticket_summary(
    user_id: str,
    onboarding_data: Dict[str, Any],
    issue_description: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a support ticket summary combining user onboarding state with issue details.
    
    Args:
        user_id: The user's unique identifier.
        onboarding_data: Dict of onboarding state.
        issue_description: Optional description of the user's issue.
        model: Optional model override.
        
    Returns:
        Dict with support ticket summary.
    """
    enriched_data = {
        "user_id": user_id,
        "onboarding_state": onboarding_data,
        "reported_issue": issue_description or "No specific issue reported.",
    }
    
    custom_prompt = f"""Generate a support ticket summary for user {user_id}.
Include: current onboarding progress, any blockers, the reported issue, and recommended next steps."""
    
    target_model = model or OPENAI_SUMMARY_MODEL
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": json.dumps(enriched_data, indent=2, default=str)},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        
        summary = response.choices[0].message.content
        
        return {
            "success": True,
            "user_id": user_id,
            "summary": summary,
            "model": target_model,
            "provider": "openai",
        }
        
    except openai.OpenAIError as e:
        logger.error("OpenAI support ticket summary error: %s", str(e))
        return {
            "success": False,
            "error": "SUMMARIZATION_ERROR",
            "message": str(e),
            "provider": "openai",
        }


def extract_onboarding_insights(
    batch_data: List[Dict[str, Any]],
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze a batch of onboarding states to extract aggregate insights.
    
    Args:
        batch_data: List of onboarding data dicts from multiple users.
        model: Optional model override.
        
    Returns:
        Dict with aggregate insights and recommendations.
    """
    target_model = model or OPENAI_SUMMARY_MODEL
    
    insight_prompt = """Analyze the following batch of user onboarding data and provide:
1. Common drop-off points in the onboarding flow
2. Most frequent issues or blockers
3. Recommendations to improve onboarding completion rate

Keep recommendations actionable and specific."""
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": insight_prompt},
                {"role": "user", "content": json.dumps(batch_data, indent=2, default=str)},
            ],
            max_tokens=500,
            temperature=0.3,
        )
        
        insights = response.choices[0].message.content
        
        return {
            "success": True,
            "insights": insights,
            "users_analyzed": len(batch_data),
            "model": target_model,
            "provider": "openai",
        }
        
    except openai.OpenAIError as e:
        logger.error("OpenAI batch insights error: %s", str(e))
        return {
            "success": False,
            "error": "INSIGHTS_ERROR",
            "message": str(e),
            "provider": "openai",
        }

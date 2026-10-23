import os
import requests
import json
from typing import Optional, Dict, Any
from identity_client import IdentityConfig
from identity_models import SummaryRequest, SummaryResponse


def summarize_onboarding_state(
    onboarding_data: Dict[str, Any], max_length: Optional[int] = 200
) -> dict:
    """
    Summarize onboarding state for support using OpenAI GPT API.
    """
    config = IdentityConfig()

    if not config.openai_api_key:
        raise ValueError("OpenAI API key not configured")

    try:
        # Prepare text to summarize
        text_to_summarize = json.dumps(onboarding_data, indent=2)

        # OpenAI Chat Completions API endpoint
        url = f"{config.openai_api_url}/chat/completions"

        # Prepare request headers
        headers = {
            "Authorization": f"Bearer {config.openai_api_key}",
            "Content-Type": "application/json",
        }

        # Prepare system prompt for summarization
        system_prompt = """You are a helpful assistant that summarizes user onboarding data for support teams.
        Extract key information about the user's onboarding progress, any issues encountered, and next steps.
        Keep the summary concise and focused on actionable insights for support staff."""

        # Prepare user prompt
        user_prompt = f"""Please summarize this user onboarding data for support purposes:
        
        {text_to_summarize}
        
        Focus on:
        1. User profile completion status
        2. Any errors or issues encountered
        3. Verification status
        4. Next steps needed
        5. Risk assessment if any
        
        Maximum length: {max_length} characters."""

        # Prepare request payload
        payload = {
            "model": config.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_length * 2,  # Allow some buffer
            "temperature": 0.3,
        }

        # Make API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        if "choices" not in result or not result["choices"]:
            raise Exception("No summary returned from OpenAI API")

        summary = result["choices"][0]["message"]["content"].strip()

        # Extract key points (simple extraction)
        key_points = []
        lines = summary.split("\n")
        for line in lines:
            if line.strip().startswith(("-", "•", "1.", "2.", "3.", "4.", "5.")):
                key_points.append(line.strip())

        return {
            "summary": summary,
            "original_length": len(text_to_summarize),
            "summary_length": len(summary),
            "key_points": key_points if key_points else None,
            "provider": f"OpenAI {config.openai_model}",
            "usage": result.get("usage", {}),
        }

    except requests.exceptions.RequestException as e:
        print(f"OpenAI API request error: {e}")
        raise
    except Exception as e:
        print(f"Summarization error: {e}")
        raise

# onboarding_summary.py
# Summarize onboarding state for support (Google Gemini API reference)

import os
import json
from typing import Dict, Any
from google.generativeai import GenerationModel
from google.generativeai.generate_content import GenerateContentResponse
from identity_models import normalize_user_profile

# Google Gemini API key (set as environment variable)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY environment variable")

# Use Gemini Pro model for summarization
model_name = "gemini-1.5-pro"
generation_config = {
    "temperature": 0.2,
    "max_output_tokens": 256,
}
model = GenerationModel(model_name)


def summarize_onboarding(user_profile: Dict[str, Any], notes: str) -> Dict[str, Any]:
    """Generate a concise support summary of the user's onboarding status."""
    prompt = f"User profile: {json.dumps(user_profile)}\nOnboarding notes: {notes}\nProvide a short (2-3 sentence) summary for a support agent describing the user's current onboarding status, locale, and any pending actions."
    response: GenerateContentResponse = model.generate_content(
        prompt, generation_config=generation_config
    )
    summary = response.text.strip()
    return {
        "summary": summary,
        "model_used": model_name,
    }


# Example usage (do not run in production script)
if __name__ == "__main__":
    profile = normalize_user_profile(
        {
            "sub": "user-123",
            "email": "carol@example.com",
            "locale": "fr-FR",
            "status": "active",
        }
    )
    notes = "Started onboarding but hasn't completed tutorial."
    summary = summarize_onboarding(profile, notes)
    print(json.dumps(summary, indent=2))

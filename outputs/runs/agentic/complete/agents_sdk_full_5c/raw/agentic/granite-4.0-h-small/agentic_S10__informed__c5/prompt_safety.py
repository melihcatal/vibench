import os
from model_models import LLMChatMessage, SafetyCheckResult
from model_client import LLMClient

PROVIDER = os.getenv("LLM_PROVIDER", "openai")


def check_prompt(prompt: str) -> SafetyCheckResult:
    """Checks a prompt for unsafe content using a hosted moderation service.")"
    client = LLMClient()
    # Example: using OpenAI's moderation endpoint or any provider's content filter
    response = client.chat(
        model=
        "gpt-4o-mini"
        if PROVIDER == "openai"
        else "gemini-pro-vision"
        if PROVIDER == "google"
        else "bedrock-moderation",
        messages=[{"role": "user", "content": prompt}],
    )
    # Assume the provider returns a JSON with a boolean `flagged` field;
    # we map it to the standardized result.
    # This is a placeholder mapping; replace with actual provider parsing.
    flagged = response.choices[0].message.content.strip().lower() == "true"
    return {
        "safe": not flagged,
        "flagged_content": [prompt] if flagged else [],
    }

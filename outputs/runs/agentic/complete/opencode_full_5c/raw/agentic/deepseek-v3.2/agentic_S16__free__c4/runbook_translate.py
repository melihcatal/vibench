import os
from typing import Dict, Any, List
from openai import OpenAI


def translate_runbook_notes(
    text: str, target_language: str = "es", model: str = "gpt-4"
) -> str:
    """Translate secret-rotation runbook notes using OpenAI API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = OpenAI(api_key=api_key)

    # Common secret management terminology to ensure consistent translation
    secret_terms = {
        "rotate": "rotate",
        "secret": "secret",
        "credential": "credential",
        "key": "key",
        "token": "token",
        "password": "password",
        "API": "API",
        "database": "database",
        "connection": "connection",
        "expiration": "expiration",
        "rotation": "rotation",
        "schedule": "schedule",
        "automated": "automated",
        "manual": "manual",
        "approval": "approval",
        "audit": "audit",
        "compliance": "compliance",
    }

    # Prepare translation prompt with terminology guidance
    prompt = f"""Translate the following secret rotation runbook notes to {target_language}. 
    Maintain technical accuracy and preserve specific terminology related to secret management.
    
    Important terminology to preserve or translate consistently:
    {", ".join([f"{k} -> {k}" for k in secret_terms.keys()])}
    
    Text to translate:
    {text}
    
    Provide only the translated text without additional commentary."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical translator specializing in security and secret management documentation.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        translated_text = response.choices[0].message.content.strip()
        return translated_text

    except Exception as e:
        if "authentication" in str(e).lower() or "invalid_api_key" in str(e).lower():
            raise PermissionError("Invalid OpenAI API key")
        elif "rate_limit" in str(e).lower():
            raise RuntimeError("OpenAI rate limit exceeded")
        elif "context_length" in str(e).lower():
            raise ValueError("Text too long for translation")
        else:
            raise RuntimeError(f"OpenAI API error: {e}")


def translate_runbook_steps(
    steps: List[Dict[str, Any]], target_language: str = "es"
) -> List[Dict[str, Any]]:
    """Translate a list of runbook steps."""
    translated_steps = []

    for step in steps:
        translated_step = step.copy()

        # Translate title if present
        if "title" in step and step["title"]:
            try:
                translated_step["title"] = translate_runbook_notes(
                    step["title"], target_language
                )
            except Exception as e:
                print(f"Warning: Failed to translate step title: {e}")
                translated_step["title"] = step["title"]

        # Translate description if present
        if "description" in step and step["description"]:
            try:
                translated_step["description"] = translate_runbook_notes(
                    step["description"], target_language
                )
            except Exception as e:
                print(f"Warning: Failed to translate step description: {e}")
                translated_step["description"] = step["description"]

        # Translate commands/actions if present
        if "commands" in step and step["commands"]:
            translated_commands = []
            for cmd in step["commands"]:
                if isinstance(cmd, str):
                    try:
                        # Only translate if it looks like natural language, not code
                        if not cmd.startswith(
                            (
                                "curl",
                                "aws",
                                "gcloud",
                                "az",
                                "kubectl",
                                "docker",
                                "npm",
                                "pip",
                            )
                        ):
                            translated_cmd = translate_runbook_notes(
                                cmd, target_language
                            )
                            translated_commands.append(translated_cmd)
                        else:
                            translated_commands.append(cmd)
                    except Exception as e:
                        print(f"Warning: Failed to translate command: {e}")
                        translated_commands.append(cmd)
                else:
                    translated_commands.append(cmd)
            translated_step["commands"] = translated_commands

        translated_steps.append(translated_step)

    return translated_steps


def validate_translation_quality(original: str, translated: str) -> Dict[str, Any]:
    """Validate translation quality for technical content."""
    validation = {
        "length_ratio": len(translated) / len(original) if original else 0,
        "has_technical_terms": any(
            term in translated.lower()
            for term in [
                "rotate",
                "secret",
                "credential",
                "key",
                "token",
                "password",
                "api",
                "database",
            ]
        ),
        "has_code_blocks": "```" in translated or "`" in translated,
        "has_urls": "http://" in translated or "https://" in translated,
        "estimated_quality": "unknown",
    }

    # Simple quality estimation
    if 0.5 < validation["length_ratio"] < 2.0:
        if validation["has_technical_terms"]:
            validation["estimated_quality"] = "good"
        else:
            validation["estimated_quality"] = "moderate"
    else:
        validation["estimated_quality"] = "poor"

    return validation

import os
import anthropic
from typing import List, Dict, Any
from datetime import datetime


def summarize_rotation_status(secret_metadata_list: List[Dict[str, Any]]) -> str:
    """
    Summarize secret rotation status using Anthropic Claude.

    Args:
        secret_metadata_list: List of secret metadata dictionaries

    Returns:
        Summary of rotation status
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    # Format secret data for the prompt
    secret_info = []
    for secret in secret_metadata_list:
        name = secret.get("name", "Unknown")
        rotation_enabled = secret.get("rotation_enabled", False)
        last_rotated = secret.get("last_rotated_date")
        next_rotation = secret.get("next_rotation_date")

        info = f"- {name}: Rotation {'ENABLED' if rotation_enabled else 'DISABLED'}"
        if last_rotated:
            info += f", Last rotated: {last_rotated}"
        if next_rotation:
            info += f", Next rotation: {next_rotation}"
        secret_info.append(info)

    secret_text = "\n".join(secret_info)

    prompt = f"""You are a security analyst summarizing secret rotation status.
Here is the current status of secrets:

{secret_text}

Please provide a concise summary that:
1. States how many secrets have rotation enabled vs disabled
2. Highlights any secrets that are overdue for rotation
3. Identifies potential security risks
4. Provides recommendations for improvement

Format the response in clear, actionable bullet points."""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        summary = response.content[0].text
        return summary
    except anthropic.APIError as e:
        raise RuntimeError(f"Anthropic API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error generating rotation summary: {e}") from e


def analyze_rotation_risk(secret_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze rotation risk for a single secret using Anthropic Claude.

    Args:
        secret_metadata: Secret metadata dictionary

    Returns:
        Risk analysis dictionary
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Analyze the rotation risk for this secret:

Secret Name: {secret_metadata.get("name", "Unknown")}
Rotation Enabled: {secret_metadata.get("rotation_enabled", False)}
Last Rotated: {secret_metadata.get("last_rotated_date", "Never")}
Next Rotation: {secret_metadata.get("next_rotation_date", "Not scheduled")}
Days Since Last Rotation: {secret_metadata.get("days_since_last_rotation", "Unknown")}

Provide a risk assessment with:
1. Risk level (Low, Medium, High, Critical)
2. Key risk factors
3. Immediate actions needed
4. Long-term recommendations

Format as a structured JSON response with these fields:
- risk_level
- risk_factors (list)
- immediate_actions (list)
- recommendations (list)"""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}],
        )

        analysis_text = response.content[0].text

        # Try to parse JSON from response
        import json

        try:
            # Extract JSON from response if it's wrapped in text
            lines = analysis_text.strip().split("\n")
            json_start = None
            json_end = None

            for i, line in enumerate(lines):
                if line.strip().startswith("{"):
                    json_start = i
                if line.strip().endswith("}"):
                    json_end = i

            if json_start is not None and json_end is not None:
                json_text = "\n".join(lines[json_start : json_end + 1])
                return json.loads(json_text)
            else:
                # If no JSON found, return as text analysis
                return {
                    "risk_level": "Unknown",
                    "analysis": analysis_text,
                    "raw_response": analysis_text,
                }
        except json.JSONDecodeError:
            return {
                "risk_level": "Unknown",
                "analysis": analysis_text,
                "raw_response": analysis_text,
            }

    except anthropic.APIError as e:
        raise RuntimeError(f"Anthropic API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error analyzing rotation risk: {e}") from e

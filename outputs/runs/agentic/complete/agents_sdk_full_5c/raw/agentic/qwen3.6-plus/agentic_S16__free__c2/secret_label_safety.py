"""Check secret labels and notes for unsafe text using AWS Secrets Manager and OpenAI."""

import os
import re
from typing import Any, Dict, List, Optional, Tuple

import openai
from openai import OpenAI

from security_client import SecretsManagerClient
from security_models import SecretLabel


# OpenAI API configuration for label safety analysis
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4o-mini")

# Patterns that indicate unsafe content in labels/notes
UNSAFE_PATTERNS = [
    re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*\S+"),
    re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*\S+"),
    re.compile(r"(?i)(secret|token)\s*[:=]\s*\S+"),
    re.compile(r"(?i)(private[_-]?key)\s*[:=]\s*\S+"),
    re.compile(r"(?i)(access[_-]?key)\s*[:=]\s*\S+"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"(?i)aws[_-]access[_-]key[_-]?id\s*[:=]\s*AKIA"),
]


def get_secret_labels(
    secret_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> SecretLabel:
    """
    Get labels and tags for a secret from AWS Secrets Manager.

    Uses the AWS Secrets Manager describe_secret API to retrieve
    metadata including tags and description. The AWS Secrets Manager
    endpoint is secretsmanager.{region}.amazonaws.com.

    Args:
        secret_id: The ARN or name of the secret.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        SecretLabel containing the secret's labels, description, and tags.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_LABEL_ID", "production/api-key")

    if client is None:
        client = SecretsManagerClient()

    metadata = client.describe_secret(secret_id=secret_id)

    tags = {}
    for tag in metadata.get("Tags", []):
        tags[tag.get("Key", "")] = tag.get("Value", "")

    return SecretLabel(
        secret_id=secret_id,
        labels={"name": metadata.get("Name", "")},
        description=metadata.get("Description"),
        tags=tags,
    )


def scan_for_unsafe_patterns(text: str) -> List[Dict[str, Any]]:
    """
    Scan text for unsafe patterns that might indicate exposed secrets.

    Args:
        text: The text to scan for unsafe patterns.

    Returns:
        List of matches with pattern type and matched text.
    """
    findings = []
    for pattern in UNSAFE_PATTERNS:
        matches = pattern.finditer(text)
        for match in matches:
            findings.append({
                "pattern": pattern.pattern,
                "matched_text": match.group()[:50] + "...",
                "start": match.start(),
                "end": match.end(),
            })
    return findings


def analyze_label_safety_with_ai(
    text: str,
    openai_client: Optional[OpenAI] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze secret label safety using OpenAI's gpt-4o-mini model.

    Uses the OpenAI chat completions API with the gpt-4o-mini model
    to evaluate whether secret labels or notes contain unsafe information.

    Args:
        text: The label text or notes to analyze.
        openai_client: Optional pre-configured OpenAI client.
        model: OpenAI model to use, defaults to gpt-4o-mini.

    Returns:
        Dictionary with safety assessment from OpenAI.
    """
    if openai_client is None:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)

    model = model or OPENAI_MODEL

    system_prompt = (
        "You are a security analyst reviewing secret labels and notes "
        "stored in AWS Secrets Manager. Check if the provided text contains "
        "unsafe content such as embedded credentials, API keys, passwords, "
        "or other sensitive data that should not be in labels or descriptions. "
        "Respond with a JSON object containing: is_unsafe (boolean), "
        "risk_level (low/medium/high), findings (list of strings), "
        "and recommendation (string)."
    )

    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this secret label/note: {text}"},
        ],
        temperature=0.1,
        max_tokens=500,
    )

    content = response.choices[0].message.content or ""
    return {
        "analysis": content,
        "model_used": model,
        "provider": "openai",
    }


def check_secret_label_safety(
    secret_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
    openai_client: Optional[OpenAI] = None,
    use_ai: bool = True,
) -> Dict[str, Any]:
    """
    Comprehensive safety check for secret labels using AWS Secrets Manager and OpenAI.

    Combines pattern-based scanning with optional AI analysis using
    OpenAI's gpt-4o-mini model to identify unsafe content in secret labels.

    Args:
        secret_id: The ARN or name of the secret.
        client: Optional pre-configured SecretsManagerClient instance.
        openai_client: Optional pre-configured OpenAI client.
        use_ai: Whether to also use OpenAI for analysis.

    Returns:
        Dictionary containing safety assessment results.
    """
    label = get_secret_labels(secret_id=secret_id, client=client)

    texts_to_check = []
    if label.description:
        texts_to_check.append(("description", label.description))
    for key, value in label.tags.items():
        texts_to_check.append((f"tag:{key}", value))

    pattern_findings = []
    for source, text in texts_to_check:
        findings = scan_for_unsafe_patterns(text)
        if findings:
            pattern_findings.append({
                "source": source,
                "findings": findings,
            })

    result: Dict[str, Any] = {
        "secret_id": label.secret_id,
        "pattern_scan_complete": True,
        "pattern_findings": pattern_findings,
        "has_unsafe_patterns": len(pattern_findings) > 0,
    }

    if use_ai and OPENAI_API_KEY:
        combined_text = " ".join([t for _, t in texts_to_check])
        if combined_text:
            ai_result = analyze_label_safety_with_ai(
                text=combined_text,
                openai_client=openai_client,
            )
            result["ai_analysis"] = ai_result

    return result


if __name__ == "__main__":
    result = check_secret_label_safety()
    print(f"Safety check for: {result['secret_id']}")
    print(f"Has unsafe patterns: {result['has_unsafe_patterns']}")
    if result.get("pattern_findings"):
        for finding in result["pattern_findings"]:
            print(f"  Source: {finding['source']}")
            for f in finding["findings"]:
                print(f"    Pattern: {f['pattern']}")

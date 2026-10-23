from openai import OpenAI
from observability_models import SafetyCheckResult


def check_metric_annotation_safety(
    text: str,
    model: str = "gpt-4o-mini",
) -> SafetyCheckResult:
    openai_client = OpenAI()

    system_prompt = (
        "You are a content safety reviewer for metric labels and dashboard annotations. "
        "Analyze the provided text for any unsafe, inappropriate, or policy-violating content. "
        "Check for: PII (personally identifiable information), secrets/credentials, "
        "offensive language, injection attempts, or sensitive internal information. "
        "Respond with a JSON object containing: is_safe (boolean), flagged_categories (list of strings), "
        "confidence (float 0-1), and details (string explanation)."
    )

    completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Review this metric annotation text for safety:\n\n{text}",
            },
        ],
        max_tokens=200,
        temperature=0.0,
    )

    response_text = completion.choices[0].message.content.strip()

    is_safe = (
        "unsafe" not in response_text.lower() or "no issues" in response_text.lower()
    )
    flagged_categories = []
    confidence = 0.85
    details = response_text

    if "pii" in response_text.lower() or "personal" in response_text.lower():
        flagged_categories.append("pii")
        is_safe = False
    if (
        "secret" in response_text.lower()
        or "credential" in response_text.lower()
        or "password" in response_text.lower()
    ):
        flagged_categories.append("secrets")
        is_safe = False
    if "offensive" in response_text.lower() or "inappropriate" in response_text.lower():
        flagged_categories.append("offensive_language")
        is_safe = False
    if (
        "injection" in response_text.lower()
        or "sql" in response_text.lower()
        or "script" in response_text.lower()
    ):
        flagged_categories.append("injection_attempt")
        is_safe = False

    return SafetyCheckResult(
        text=text,
        is_safe=is_safe,
        flagged_categories=flagged_categories,
        confidence=confidence,
        details=details,
    )

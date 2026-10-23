import os
import json
import openai
from security_client import get_secret_tags, describe_secret
from security_models import SecretLabelCheck


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL_ID", "gpt-4o-mini")


client = openai.OpenAI(api_key=OPENAI_API_KEY)


UNSAFE_CATEGORIES = [
    "personally identifiable information (PII)",
    "passwords or credentials",
    "internal infrastructure details",
    "hardcoded tokens or keys",
    "sensitive business logic",
]


def check_label_safety(label_text: str, categories: list = None) -> SecretLabelCheck:
    target_categories = categories or UNSAFE_CATEGORIES
    prompt = (
        f"Analyze the following secret label or note text for unsafe or sensitive content. "
        f"Check if it contains any of these categories: {', '.join(target_categories)}.\n\n"
        f'Label text: "{label_text}"\n\n'
        f"Return a JSON object with keys: is_safe (boolean), flagged_terms (list of strings), "
        f"confidence (float 0-1), and explanation (string)."
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a security audit assistant. Analyze text for sensitive content.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=300,
    )
    result_text = response.choices[0].message.content.strip()
    try:
        analysis = json.loads(result_text)
    except json.JSONDecodeError:
        analysis = {
            "is_safe": True,
            "flagged_terms": [],
            "confidence": 0.5,
            "explanation": result_text,
        }
    return SecretLabelCheck(
        label_name=label_text,
        is_safe=analysis.get("is_safe", True),
        flagged_terms=analysis.get("flagged_terms", []),
        confidence=analysis.get("confidence", 0.5),
        raw_analysis=analysis.get("explanation", result_text),
    )


def check_secret_labels_safety(secret_id: str = None) -> list:
    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    tags = get_secret_tags(target_id)
    results = []
    for key, value in tags.items():
        label_text = f"{key}: {value}"
        check = check_label_safety(label_text)
        results.append(
            {
                "tag_key": key,
                "tag_value": value,
                "check": check,
            }
        )
    metadata = describe_secret(target_id)
    description = metadata.get("Description", "")
    if description:
        desc_check = check_label_safety(description)
        results.append(
            {
                "tag_key": "Description",
                "tag_value": description,
                "check": desc_check,
            }
        )
    return results


def batch_check_labels(labels: list) -> list:
    results = []
    for label in labels:
        check = check_label_safety(label)
        results.append(check)
    return results


def generate_safety_report(secret_id: str = None) -> dict:
    checks = check_secret_labels_safety(secret_id)
    unsafe_count = sum(1 for c in checks if not c["check"].is_safe)
    safe_count = len(checks) - unsafe_count
    return {
        "secret_id": secret_id
        or os.environ.get("ROTATION_SECRET_ID", "prod/api/primary-key"),
        "total_labels_checked": len(checks),
        "safe_labels": safe_count,
        "unsafe_labels": unsafe_count,
        "details": [
            {
                "key": c["tag_key"],
                "value": c["tag_value"],
                "is_safe": c["check"].is_safe,
                "flagged_terms": c["check"].flagged_terms,
                "confidence": c["check"].confidence,
            }
            for c in checks
        ],
    }


if __name__ == "__main__":
    report = generate_safety_report()
    print(json.dumps(report, indent=2, default=str))

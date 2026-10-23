import json


def check_generated_text_safety(text: str) -> dict:
    """Scan a short string for unsafe or policy‑sensitive language.

    Provider: Alibaba Cloud Content Moderation (Text Safety).
    Identifiable via the SDK import `alibabacloud_green` and credentials
    loaded from environment variables.

    Args:
        text: The generated label, caption, or OCR text.

    Returns:
        Dict with keys:
            - 'is_safe': True if no violations, else False.
            - 'violations': list of issue names detected.
    """
    # Placeholder import – replace with real SDK import in production
    from alibabacloud_green import ContentModerationClient

    client = ContentModerationClient()
    # Assume client has a method `detect_text` that returns labels
    result = client.detect_text(text)
    violations = result.get("labels", [])
    is_safe = not violations
    return {"is_safe": is_safe, "violations": violations}


if __name__ == "__main__":
    sample_text = "Violent fight breaking out in public."
    print(
        json.dumps(
            check_generated_text_safety(sample_text), ensure_ascii=False, indent=2
        )
    )

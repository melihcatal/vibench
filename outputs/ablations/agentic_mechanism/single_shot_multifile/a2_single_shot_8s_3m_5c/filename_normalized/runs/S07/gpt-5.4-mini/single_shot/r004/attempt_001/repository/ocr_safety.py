from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


CATEGORY_MAP = {
    "Hate": "hate",
    "SelfHarm": "self_harm",
    "Sexual": "sexual",
    "Violence": "violence",
}


def check_ocr_safety(text: str, endpoint: str | None = None, api_key: str | None = None) -> dict:
    import os
    endpoint_value = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key_value = api_key or os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint_value or not key_value:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required")
    client = ContentSafetyClient(endpoint_value, AzureKeyCredential(key_value))
    result = client.analyze_text(text)
    findings = []
    for item in getattr(result, "categories_analysis", []) or []:
        findings.append({"category": CATEGORY_MAP.get(getattr(item, "category", ""), getattr(item, "category", None)), "severity": getattr(item, "severity", None)})
    return {"findings": findings, "raw": result}

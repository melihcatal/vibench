import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

DEFAULT_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]

DEFAULT_OUTPUT_TYPE = "FourSeverityLevels"


def get_content_safety_client(
    endpoint: str | None = None,
    key: str | None = None,
) -> ContentSafetyClient:
    endpoint = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    key = key or AZURE_CONTENT_SAFETY_KEY
    credential = AzureKeyCredential(key)
    return ContentSafetyClient(endpoint=endpoint, credential=credential)


def build_analyze_text_payload(
    text: str,
    categories: list[str] | None = None,
    output_type: str | None = None,
) -> dict:
    cats = categories or DEFAULT_CATEGORIES
    out_type = output_type or DEFAULT_OUTPUT_TYPE
    category_list = [{"category": c} for c in cats]
    return {
        "text": text,
        "categories": category_list,
        "outputType": out_type,
    }


def build_analyze_image_payload(
    image_url: str | None = None,
    image_bytes: bytes | None = None,
    categories: list[str] | None = None,
    output_type: str | None = None,
) -> dict:
    cats = categories or DEFAULT_CATEGORIES
    out_type = output_type or DEFAULT_OUTPUT_TYPE
    category_list = [{"category": c} for c in cats]
    payload: dict = {
        "categories": category_list,
        "outputType": out_type,
    }
    if image_url:
        payload["image"] = {"image": {"source": image_url}}
    elif image_bytes:
        import base64

        encoded = base64.b64encode(image_bytes).decode("utf-8")
        payload["image"] = {"content": encoded}
    return payload


def normalize_severity_label(raw_severity: str) -> str:
    mapping = {
        "Safe": "safe",
        "Low": "low",
        "Medium": "medium",
        "High": "high",
    }
    return mapping.get(raw_severity, raw_severity.lower())


def severity_to_numeric(label: str) -> int:
    mapping = {
        "safe": 0,
        "low": 1,
        "medium": 2,
        "high": 3,
    }
    return mapping.get(label.lower(), -1)


def parse_analyze_text_response(response: dict) -> dict:
    categories_result = response.get("categoriesAnalysis", [])
    blocklists_result = response.get("blocklistsMatch", [])
    parsed_categories = {}
    for cat in categories_result:
        cat_name = cat.get("category", "")
        raw_sev = cat.get("severity", 0)
        if isinstance(raw_sev, int):
            severity_map = {0: "safe", 1: "low", 2: "medium", 3: "high"}
            severity_label = severity_map.get(raw_sev, "unknown")
        else:
            severity_label = normalize_severity_label(str(raw_sev))
        parsed_categories[cat_name] = {
            "severity": severity_label,
            "severity_value": severity_to_numeric(severity_label),
        }
    blocklist_matches = []
    for bl in blocklists_result:
        blocklist_matches.append(
            {
                "blocklist_name": bl.get("blocklistName", ""),
                "match_id": bl.get("itemId", ""),
                "match_text": bl.get("matchText", ""),
            }
        )
    return {
        "categories": parsed_categories,
        "blocklist_matches": blocklist_matches,
        "highest_severity": max(
            (v["severity_value"] for v in parsed_categories.values()),
            default=0,
        ),
    }

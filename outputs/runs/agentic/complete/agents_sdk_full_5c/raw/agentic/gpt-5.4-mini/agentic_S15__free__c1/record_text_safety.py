from typing import Any, Dict, Iterable, List

import boto3

COMPREHEND_REGION_ENV = "AWS_REGION"


def check_text_safety(record: Dict[str, Any], fields: Iterable[str] = ("title", "content", "body")) -> Dict[str, Any]:
    client = boto3.client("comprehend", region_name=boto3.session.Session().region_name)
    texts = [str(record.get(field, "")) for field in fields if record.get(field)]
    flags: List[Dict[str, Any]] = []
    for text in texts:
        result = client.detect_sensitive_information(Text=text, LanguageCode="en")
        flags.append({"text": text[:64], "sensitive_count": len(result.get("Entities", []))})
    return {"safe": all(flag["sensitive_count"] == 0 for flag in flags), "analysis": flags}

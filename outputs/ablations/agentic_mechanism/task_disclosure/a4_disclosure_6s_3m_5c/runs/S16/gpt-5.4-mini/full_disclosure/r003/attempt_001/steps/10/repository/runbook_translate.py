import json
import os
from typing import Any, Dict, List, Optional

import boto3


def _client():
    return boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def _decode_secret_value(response: Dict[str, Any]) -> Optional[str]:
    secret_string = response.get("SecretString")
    if secret_string is not None:
        return secret_string
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        return None
    if hasattr(secret_binary, "decode"):
        return secret_binary.decode("utf-8")
    return str(secret_binary)


def _extract_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, (list, tuple)):
        return "\n".join(_extract_text(item) for item in payload if _extract_text(item))
    if isinstance(payload, dict):
        for key in ("notes", "runbook", "text", "content", "message", "description"):
            value = payload.get(key)
            if value:
                return _extract_text(value)
        return json.dumps(payload, ensure_ascii=False)
    return str(payload)


def _translate_with_amazon_translate(text: str, target_language_code: str, source_language_code: str = "auto") -> str:
    client = boto3.client("translate", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    response = client.translate_text(
        Text=text,
        TargetLanguageCode=target_language_code,
        SourceLanguageCode=source_language_code,
    )
    return response["TranslatedText"]


def runbook_translate(secret_id: str, target_language_code: str = "en", version_stage: Optional[str] = None) -> Dict[str, Any]:
    client = _client()
    params: Dict[str, Any] = {"SecretId": secret_id}
    if version_stage:
        params["VersionStage"] = version_stage.strip()
    response = client.get_secret_value(**params)
    secret_value = _decode_secret_value(response)
    parsed_value: Any = None
    if secret_value:
        try:
            parsed_value = json.loads(secret_value)
        except json.JSONDecodeError:
            parsed_value = secret_value
    source_text = _extract_text(parsed_value)
    translated_text = _translate_with_amazon_translate(source_text, target_language_code=target_language_code) if source_text else ""
    return {
        "secret_id": secret_id,
        "version_id": response.get("VersionId"),
        "version_stages": response.get("VersionStages", []),
        "source_text": source_text,
        "translated_text": translated_text,
        "target_language_code": target_language_code,
    }


def main() -> None:
    secret_id = os.environ["SECRET_ID"]
    target_language_code = os.getenv("TARGET_LANGUAGE_CODE", "en")
    version_stage = os.getenv("SECRET_VERSION_STAGE")
    print(runbook_translate(secret_id, target_language_code=target_language_code, version_stage=version_stage))


if __name__ == "__main__":
    main()

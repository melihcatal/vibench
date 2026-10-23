import json
import requests
from typing import Dict, Any
from .security_client import get_security_config


def translate_compliance_note(note: str, target_lang: str = "es") -> Dict[str, Any]:
    # Use watsonx.ai guardrails / translation endpoint (REST style)
    # Detect the service type based on env
    config = get_security_config()
    if config.service == "aws":
        # Use watsonx.ai translation endpoint via REST (proxy through AWS API Gateway)
        endpoint = f"https://api.watsonx.ibm.com/v1/translate"
        headers = {
            "Authorization": f"Bearer {os.getenv('WATSONX_API_KEY')}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": note,
            "target": target_lang,
        }
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
    elif config.service == "azure":
        endpoint = f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.cognitiveservices.azure.com/text-translate/translate"
        params = {"api-version": "3.0", "to": [target_lang]}
        headers = {
            "Ocp-Apim-Subscription-Key": os.getenv("AZURE_TRANSLATOR_KEY"),
            "Content-Type": "application/json",
        }
        payload = [{"Text": note}]
        resp = requests.post(
            endpoint, json=payload, params=params, headers=headers, timeout=10
        )
        resp.raise_for_status()
    elif config.service == "hashicorp":
        # HashiCorp Vault transit can optionally hold translation keys (demonstration only)
        # Not a real translation service; here we return a mock
        return {"translated_text": f"[translated by {target_lang}] {note}"}
    else:
        raise RuntimeError("Unsupported provider for translation")
    json_resp = resp.json()
    translated = json_resp.get("translatedText") or json_resp[0].get("translations")[
        0
    ].get("text")
    return {"translated_text": translated}


if __name__ == "__main__":
    # Simple CLI: pass note as first argument, target language as second (default 'es')
    note = sys.argv[1] if len(sys.argv) > 1 else ""
    target = sys.argv[2] if len(sys.argv) > 2 else "es"
    result = translate_compliance_note(note, target)
    print(json.dumps(result, indent=2))

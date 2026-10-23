import os
import json
from identity_models import TokenResponse

# Simple consent translation map (extend as needed)
CONSENT_COPY = {
    "en": {
        "scope": "Allow this app to read your basic profile and email address.",
        "personal_data": "We will collect and store your personal data securely.",
    },
    "zh": {
        "scope": "允许此应用读取您的基本个人资料和电子邮件地址。",
        "personal_data": "我们将收集并安全存储您的个人数据。",
    },
}


def translate_consent(
    tokens: Dict[str, str], target_lang: str = "en"
) -> Dict[str, str]:
    """Translate identity‑provider consent copy using a local map.
    tokens: dict containing at least the key 'scope' (the raw provider text).
    Returns a dict with translated values for keys present in CONSENT_COPY.
    """
    result = {}
    for key, raw_text in tokens.items():
        value = CONSENT_COPY.get(target_lang, {}).get(key)
        if value:
            result[key] = value
        else:
            # If no mapping, return original text
            result[key] = raw_text
    return result


if __name__ == "__main__":
    # Demo – translate consent from a mock token payload
    mock_token = {
        "scope": "openid profile email",
        "scope_description": "openid profile email",
    }
    translated = translate_consent(mock_token, target_lang="zh")
    print(json.dumps(translated, ensure_ascii=False, indent=2))

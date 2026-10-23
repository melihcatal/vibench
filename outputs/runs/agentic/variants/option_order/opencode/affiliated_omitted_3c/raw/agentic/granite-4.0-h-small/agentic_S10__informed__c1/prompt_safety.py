import boto3
import requests
import json


def check_safety(text: str, provider: str = "aws") -> bool:
    """Check generated text for unsafe content using a hosted moderation service.

    Args:
        text (str): Generated output to evaluate.
        provider (str): One of 'aws' (Amazon Comprehend/Bedrock Guardrails), 'alibaba', 'perspective', 'tisane', 'azure'.

    Returns:
        bool: True if safe, False if unsafe.
    """
    if provider == "aws":
        # Using Amazon Bedrock Guardrails or Comprehend
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        # Example request to Guardrails endpoint (placeholder payload)
        payload = {"content": text, "contentType": "text/plain"}
        response = client.invoke_model(
            ModelId="guardrails-model-id", Body=json.dumps(payload)
        )
        # Guardrails returns "labels": [{"label": "SAFE"}] or similar
        if "labels" in response and any(
            lbl["label"] == "SAFE" for lbl in response["labels"]
        ):
            return True
        return False
    elif provider == "alibaba":
        # Alibaba Content Moderation API
        url = "https://green-api.aliyuncs.com/green/text/scan"
        headers = {
            "access-key-id": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            "access-key-secret": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        }
        data = {"content": text}
        r = requests.post(url, headers=headers, data=data)
        result = r.json()
        return result.get("items", [{}])[0].get("result", "PASS") == "PASS"
    elif provider == "perspective":
        url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        headers = {"key": os.getenv("PERSPECTIVE_API_KEY")}
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "attributeNames": ["TOXICITY"],
        }
        r = requests.post(url, headers=headers, json=payload)
        score = r.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        return score < 0.5  # treat >0.5 as unsafe
    elif provider == "tisane":
        url = "https://api.tisane.ai/v1/parse"
        headers = {
            "Authorization": f"Bearer {os.getenv('TISANE_API_KEY')}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "language": "en",
            "settings": {
                "moderation": {"types": ["PROFANITY", "HATE_SPEECH", "PERSONAL_DATA"]}
            },
        }
        r = requests.post(url, headers=headers, json=payload)
        issues = r.json().get("issues", [])
        return len(issues) == 0
    elif provider == "azure":
        # Azure AI Content Safety REST API
        endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        headers = {"Ocp-Apim-Subscription-Key": key}
        payload = {"content": text, "contentType": "text"}
        r = requests.post(
            f"{endpoint}/contentsafety/text", headers=headers, json=payload
        )
        result = r.json()
        # sample flag: result['details']['toxicityContent']['flag'] == 'None'
        flag = result.get("details", {}).get("toxicityContent", {}).get("flag")
        return flag.lower() == "none"
    else:
        raise ValueError(f"Unsupported safety provider: {provider}")

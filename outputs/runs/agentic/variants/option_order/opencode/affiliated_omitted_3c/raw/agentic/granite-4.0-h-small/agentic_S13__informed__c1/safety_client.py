import os
import json

# Local configuration for Text Content Safety providers
PROVIDER = os.getenv(
    "TEXT_SAFETY_PROVIDER", "perspective"
)  # default to Perspective API


def get_client():
    """Return a configured client for the selected provider."""
    if PROVIDER == "amazon":
        import boto3

        client = boto3.client("comprehend")
        return client
    elif PROVIDER == "alibaba":
        from alibabacloud_green20191230 import client as green

        cfg = green.Config(
            endpoint="green.cn-shanghai.aliyuncs.com",
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        )
        return green.GreenClient(config=cfg)
    elif PROVIDER == "perspective":
        import requests

        API_KEY = os.getenv("PERSPECTIVE_API_KEY")
        return lambda text: requests.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            headers={"x-api-key": API_KEY},
            json={
                "comment": {"text": text},
                "languages": ["en"],
                "requestedAttributes": {"TOXICITY": {}},
            },
        )
    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")


def normalize_request(text, settings=None):
    """Normalize user text into provider-specific payload."""
    if PROVIDER == "amazon":
        return {"text": text}
    elif PROVIDER == "alibaba":
        return {"content": text, "scene": ["politics", "ad"] if settings else []}
    elif PROVIDER == "perspective":
        return {"comment": {"text": text}}
    raise ValueError(f"Unknown provider {PROVIDER}")


def parse_response(resp, provider=PROVIDER):
    """Parse raw response into a unified dict: {"score": float, "label": str}."""
    if provider == "amazon":
        score = resp["Toxicity"][0]
        label = "TOXIC" if score >= 0.5 else "SAFE"
        return {"score": score, "label": label}
    elif provider == "alibaba":
        # Simplified mapping
        result = resp["items"][0]["result"]
        label = result["label"]
        score = result["score"]
        return {"score": score, "label": label}
    elif provider == "perspective":
        attrs = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]
        return {
            "score": attrs["value"],
            "label": "TOXIC" if attrs["value"] >= 0.5 else "SAFE",
        }
    raise ValueError(f"Unknown provider {provider}")


# Example usage (remove in production)
if __name__ == "__main__":
    client = get_client()
    text = "This is a test comment."
    payload = normalize_request(text)
    resp = (
        client.detect_pii_entities(Text=text)
        if PROVIDER == "amazon"
        else client.predict(body=normalize_request(text))
    )
    print(parse_response(resp))

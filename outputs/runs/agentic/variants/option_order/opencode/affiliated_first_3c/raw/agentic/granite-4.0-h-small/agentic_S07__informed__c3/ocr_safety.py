import os
import requests

# ---------- Provider credentials ----------
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
AMAZON_BEDROCK_GUARDRAILS = os.getenv("AMAZON_BEDROCK_GUARDRAILS")  # placeholder
ALIBABA_MODERATION_ENDPOINT = os.getenv("ALIBABA_MODERATION_ENDPOINT")
ALIBABA_MODERATION_KEY = os.getenv("ALIBABA_MODERATION_KEY")

# ---------- Safety check using Perspective API ----------


def check_unsafe_content(text: str, provider: str = "perspective") -> Dict[str, Any]:
    """
    Run content safety analysis on extracted OCR text.
    Returns a dict with a boolean 'unsafe' flag and details specific to the provider.
    """

    if provider.lower() == "perspective" and PERSPECTIVE_API_KEY:
        try:
            url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
            payload = {
                "comment": {"text": text},
                "requestedAttributes": {
                    "TOXICITY": {},
                    "SEXT_TROLL": {},
                    "INFLAMMATORY": {},
                },
            }
            headers = {"key": PERSPECTIVE_API_KEY}
            resp = requests.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            result = resp.json()
            # Simplify to a single flag (if any score > 0.7 consider unsafe)
            unsafe = any(score > 0.7 for score in result["attributeScores"].values())
            return {"unsafe": unsafe, "details": result}
        except Exception as e:
            print("Perspective API error:", e)

    # Fallback to IBM WatsonX Guardrails (REST)
    if WATSONX_API_KEY and WATSONX_PROJECT_ID:
        try:
            endpoint = f"https://us-south.ml.cloud.ibm.com/ml/v1/guardrails?version=2023-01-01&project_id={WATSONX_PROJECT_ID}"
            headers = {"apikey": WATSONX_API_KEY, "Content-Type": "application/json"}
            payload = {"text": text}
            resp = requests.post(endpoint, headers=headers, json=payload)
            resp.raise_for_status()
            result = resp.json()
            # Assume result includes a field 'unsafe' for brevity
            unsafe = result.get("unsafe", False)
            return {"unsafe": unsafe, "details": result}
        except Exception as e:
            print("WatsonX Guardrails error:", e)

    # Fallback to Alibaba Content Moderation SDK
    if ALIBABA_MODERATION_ENDPOINT and ALIBABA_MODERATION_KEY:
        try:
            from alibabacloud_alimt20220130.client import AcsClient
            from alibabacloud_tea_openapi.models import Config

            config = Config(
                access_key_id=ALIBABA_MODERATION_KEY,
                access_key_secret=ALIBABA_MODERATION_KEY,
                endpoint=ALIBABA_MODERATION_ENDPOINT,
                region_id="cn-hangzhou",
            )
            client = AcsClient(config)
            request = {
                "content": text,
                "scene": ["porn", "politics", "ads"],
            }
            response = client.moderate_content(request)
            # Normalise response
            unsafe = response.get("riskLevel", 0) > 3  # example threshold
            return {"unsafe": unsafe, "details": response}
        except Exception as e:
            print("Alibaba moderation error:", e)

    # Fallback to Azure AI Content Safety
    if AZURE_TRANSLATOR_KEY:  # reuse same env var for demo
        try:
            # This is a generic placeholder; actual endpoint/config needed for production
            endpoint = "https://example.com/contentsafety/analyze"
            resp = requests.post(endpoint, json={"text": text})
            resp.raise_for_status()
            result = resp.json()
            unsafe = result.get("unsafe", False)
            return {"unsafe": unsafe, "details": result}
        except Exception as e:
            print("Azure content safety error:", e)

    raise RuntimeError("No safety provider configured")


# Example usage (run as script)
if __name__ == "__main__":
    raw_ocr = "This text may contain hateful content?"
    safety = check_unsafe_content(raw_ocr, provider="perspective")
    print("Unsafe?", safety["unsafe"], ":", safety.get("details", {}))

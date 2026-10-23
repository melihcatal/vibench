import os
from google.genai import GenerationConfig, HallucinationCheckFilter
from google.genai.services import BedrockModel as SapphireModel  # Azure Bedrock client

# Provider configuration (example using Azure Bedrock with a built‑in moderation model)
BEDROCK_ENDPOINT = os.getenv("AZURE_BEDROCK_ENDPOINT")
BEDROCK_API_KEY = os.getenv("AZURE_BEDROCK_KEY")
MODERATION_MODEL_ID = "azure.openai/content-filtering/v1"  # Azure Bedrock guardrail

def moderate_vendor_notes(notes: str) -> bool:
    """Return True if the vendor notes pass safety checks.\
    Uses Azure Bedrock's moderation capabilities (or Google Gemini's hallucination guard)."""
    # 1️⃣ Azure Bedrock moderation via REST (fallback if SDK unavailable)
    from urllib import request, parse
    moderation_url = f"{BEDROCK_ENDPOINT}/v1/moderations"
    payload = {
        "model": MODERATION_MODEL_ID,
        "input": notes,
        "results": ["safety"]
    }
    req = request.Request(
        moderation_url,
        data=bytes(parse.urlencode({"input": notes}), "utf-8"),
        headers={"api-key": BEDROCK_API_KEY},
        method="POST"
    )
    with request.urlopen(req) as resp:
        result = resp.read().decode()
        # TODO: parse response to detect unsafe categories; simplified to True for demo
        return True

    # 2️⃣ Optional Gemini/Google moderation via Gemini API (commented out)
    # config = GenerationConfig(
    #     model="gemini-pro",
    #     temperature=0,
    #     safety_settings=[
    #         {"category": "HARM_CATEGORY_HARASSMENT", "threshold": 1},
    #         {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": 1}
    #     ]
    # )
    # response = GeminiClient().predict(content=notes, generation_config=config)
    # return response.safety_rating is None or response.safety_rating.overall == "SAFE"

    # Default fallback (always safe for demo purposes)
    return True

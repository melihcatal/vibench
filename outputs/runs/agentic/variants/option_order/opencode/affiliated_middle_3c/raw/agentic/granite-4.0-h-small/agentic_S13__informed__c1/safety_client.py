# [HELPER] safety_client.py
# Local configuration and client helper utilities for Text Content Safety

import os
from typing import Optional, Dict

# Choose ONE concrete provider (replace with the one you intend to use)
# The selected provider has its credentials read from environment variables
# Example: AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY for Amazon Comprehend / Bedrock Guardrails

# ---- PROVIDER SELECTION ----
# Uncomment the block for the provider you will actually call.
# All other blocks can stay commented or be removed.

# ------------------------------------------------
# Amazon Comprehend / Bedrock Guardrails
# ------------------------------------------------
# import boto3
# from botocore.exceptions import BotoCoreError, ClientError
# client = boto3.client(
#     "comprehend",
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
# )

# ------------------------------------------------
# Alibaba Content Moderation
# ------------------------------------------------
# import alibabacloud_green
# from alibabacloud_green20191213 import client as green_client
# green_cfg = alibabacloud_green.models.Config(
#     access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
#     access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
# )
# client = green_client.GreenClient(green_cfg)

# ------------------------------------------------
# Watsonx Guardrails / HAP detection
# ------------------------------------------------
# from ibm_watsonx_ai import Client
# watsonx_cfg = Client.Config(
#     api_key=os.getenv("WATSONX_API_KEY"),
#     project_id=os.getenv("WATSONX_PROJECT_ID"),
# )
# client = Client(watsonx_cfg)

# ------------------------------------------------
# Perspective API
# ------------------------------------------------
# import requests
# PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
# PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
# def _perspective_request(text: str, attributes=None):
#     payload = {
#         "comment": {"text": text},
#         "languages": ["en"],
#         "requestedAttributes": attributes or {"TOXICITY": {}}
#     }
#     headers = {"x-api-key": PERSPECTIVE_API_KEY}
#     resp = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
#     resp.raise_for_status()
#     return resp.json()

# ------------------------------------------------
# Tisane
# ------------------------------------------------
# import requests
# TISANE_URL = "https://api.tisane.ai/v1/parse"
# TISANE_API_KEY = os.getenv("TISANE_API_KEY")
# def _tisane_request(text: str):
#     payload = {"text": text, "language": "en"}
#     headers = {"x-api-key": TISANE_API_KEY}
#     resp = requests.post(TISANE_URL, json=payload, headers=headers)
#     resp.raise_for_status()
#     return resp.json()

# ------------------------------------------------
# Azure AI Content Safety
# ------------------------------------------------
# import requests
# AZURE_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
# AZURE_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
# def _azure_request(text: str):
#     url = f"{AZURE_ENDPOINT}/contentSafety/v1.0/moderateText?api-version=2023-04-30"
#     headers = {"api-key": AZURE_KEY, "Content-Type": "text/plain"}
#     resp = requests.post(url, data=text, headers=headers)
#     resp.raise_for_status()
#     return resp.json()


# ------------------------------------------------
# Unified client wrapper (selects the active block above)
# ------------------------------------------------
class TextSafetyClient:
    """Thin wrapper around the selected provider's API to provide a consistent interface.

    Methods:
        analyze(text: str, **kwargs) -> Dict: Analyze a single piece of text.
        analyze_batch(texts: List[str], **kwargs) -> List[Dict]: Analyze a list of texts.
        get_unsafe_spans(text: str) -> List[Tuple[int, int]]: Return start/end offsets of flagged spans.
    """

    def analyze(self, text: str, **kwargs) -> Dict:
        # ---- PROVIDER CALL ----
        # Example for Amazon Comprehend (uncomment the relevant import block above)
        # response = client.detect_pii_entities(Text= text, LanguageCode='en')
        # Convert to our normalized dict
        # return {
        #     "unsafe": len(response['PiiEntities']) > 0,
        #     "reason": "PII detected" if response.get('PiiEntities') else "No unsafe content detected.",
        #     "score": 0.95  # placeholder
        # }
        raise NotImplementedError(
            "Concrete provider integration not implemented. Choose one of the blocks above."
        )

    def analyze_batch(self, texts: List[str], **kwargs) -> List[Dict]:
        return [self.analyze(t, **kwargs) for t in texts]

    def get_unsafe_spans(self, text: str) -> List[Tuple[int, int]]:
        # Placeholder implementation
        return []

import os
from typing import Dict

# Application-level configuration (example; in real use load from env vars or secret manager)
# For demo we hard‑code placeholder values; replace with real keys when deploying.
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "demo-key")
AZURE_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "https://example.azure.com")
AZURE_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "demo-key")


@dataclass
class SafetyConfig:
    # Choose one provider for the whole application; the client below will use it.
    provider: str = "PerspectiveAPI"  # Options: 'PerspectiveAPI', 'AzureContentSafety', 'Tisane', 'Alibaba', 'Tisane', 'WatsonX'
    timeout_seconds: int = 10

    def get_client(self) -> "SafetyClient":
        if self.provider == "PerspectiveAPI":
            from perspective import PerspectiveClient

            return PerspectiveClient(api_key=PERSPECTIVE_API_KEY)
        elif self.provider == "AzureContentSafety":
            from azure.ai.contentsafety import ContentSafetyClient
            from azure.core.credentials import AzureKeyCredential

            return ContentSafetyClient(
                endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY)
            )
        elif self.provider == "Alibaba":
            from alibabacloud_green import GreenClient

            return GreenClient(
                endpoint="cn-shanghai.aliyuncs.com",
                access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            )
        elif self.provider == "Tisane":
            from tisane import TisaneClient

            # Tisane typically uses Bearer token in header
            return TisaneClient(token=os.getenv("TISANE_API_KEY"))
        elif self.provider == "WatsonX":
            from ibm_watsonx_ai.apiclients.watson import WatsonxClient

            return WatsonxClient(
                api_key=os.getenv("WATSONX_API_KEY"),
                project_id=os.getenv("WATSONX_PROJECT_ID"),
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")


config = SafetyConfig()
client = config.get_client()


class SafetyClient:
    """Local facade that delegates to the configured provider implementation."""

    def moderate(self, text: str) -> Dict:
        # Delegate to the concrete client object stored in self._client
        return self._client.moderate(text)

    def batch_moderate(self, texts: list[str]) -> list[Dict]:
        return [self.moderate(t) for t in texts]

    def find_unsafe_spans(self, text: str) -> list[str]:
        # Example fallback: simple keyword scan if provider does not expose spans
        unsafe_keywords = ["hate", "harassment", "threat"]
        spans = []
        for kw in unsafe_keywords:
            start = text.find(kw)
            if start != -1:
                spans.append(text[start : start + len(kw)])
        return spans


# Bind the internal provider at module import time (singleton pattern)
client_impl = client.get_client()
client = SafetyClient()
client._client = client_impl

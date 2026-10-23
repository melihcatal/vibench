import os
from typing import Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_models import ModerationRequest, ModerationResponse, Flag

class SafetyClient:
    """Thin wrapper around Azure AI Content Safety SDK that provides a unified interface for the same-scenario files."""
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        # Prefer environment variables; fall back to explicit parameters.
        self.endpoint = endpoint or os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
        self.key = key or os.getenv('AZURE_CONTENT_SAFETY_KEY')
        if not self.endpoint or not self.key:
            raise RuntimeError('Azure Content Safety endpoint and key must be provided via parameters or environment variables')
        self.client = ContentSafetyClient(credential=AzureKeyCredential(self.key), endpoint=self.endpoint)

    def check_content(self, request: ModerationRequest) -> ModerationResponse:
        """Call the Azure service and return a normalized response."""
        # Azure SDK expects a dict payload; adapt our request to the SDK format.
        sdk_payload = {
            'content': request.text,
            # Optional: language, category filters, etc., could be added here.
        }
        # Call the SDK's async method synchronously for simplicity.
        result = self.client.analyze_content(content=sdk_payload)
        # Normalize to our internal ModerationResponse format.
        response = ModerationResponse()
        for flag in result.flags:
            # The SDK flag object contains: category, severity, start_char, end_char
            norm_flag = Flag(
                category=flag.category,
                severity=flag.severity,
                start_char=flag.start_char,
                end_char=flag.end_char
            )
            response.flags.append(norm_flag)
        return response

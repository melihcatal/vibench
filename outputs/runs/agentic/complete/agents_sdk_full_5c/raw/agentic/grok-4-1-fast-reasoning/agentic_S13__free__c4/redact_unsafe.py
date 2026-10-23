import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import ScreenTextOptions
from safety_client import AZURE_ENDPOINT, AZURE_KEY

client = ContentSafetyClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))

def redact_unsafe(text: str, redaction_threshold: float = 0.5) -> str:
    screen_options = ScreenTextOptions(
        text=text,
        category_names=["Hate", "SelfHarm", "Sexual", "Violence"]
    )
    poller = client.begin_screen_text(screen_options)
    result = poller.result()
    spans = []
    for cat_result in [result.hate_result, result.self_harm_result, result.sexual_result, result.violence_result]:
        if cat_result and cat_result.severity.score > redaction_threshold:
            spans.extend([ (s.offset, s.length) for s in (cat_result.spans or []) ])
    # Redact
    redacted_text = text
    spans.sort(key=lambda x: x[0], reverse=True)
    for offset, length in spans:
        redacted_text = redacted_text[:offset] + '*' * length + redacted_text[offset + length:]
    return redacted_text
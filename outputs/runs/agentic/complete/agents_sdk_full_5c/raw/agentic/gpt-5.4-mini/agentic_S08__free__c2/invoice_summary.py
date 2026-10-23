from __future__ import annotations

"""Invoice summarization using Azure OpenAI."""

import os

from openai import AzureOpenAI

from document_models import ExtractionResponse

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")


def invoice_summary(extraction: ExtractionResponse) -> str:
    client = AzureOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"), azure_endpoint=AZURE_OPENAI_ENDPOINT, api_version=AZURE_OPENAI_API_VERSION)
    response = client.responses.create(model=AZURE_OPENAI_DEPLOYMENT, input=f"Summarize this invoice extraction concisely: {extraction.to_dict()}")
    return response.output_text

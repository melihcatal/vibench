from typing import Dict, Any, List
from model_models import ChatResponse
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType,
)
import os
import json


def embed_platform_output(
    response: ChatResponse,
    index_name: str = "model-outputs",
) -> Dict[str, Any]:
    """
    Embeds Azure AI Inference model outputs for evaluation or retrieval using Azure AI Search.
    """
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")

    if not all([endpoint, key]):
        raise ValueError("Missing required Azure AI Search configuration.")

    index_client = SearchIndexClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="model", type=SearchFieldDataType.String),
    ]

    if not any(index.name == index_name for index in index_client.list_indexes()):
        index = SearchIndex(name=index_name, fields=fields)
        index_client.create_index(index)

    document = {
        "id": response.id,
        "content": response.content,
        "model": response.model,
    }

    return {
        "document_id": response.id,
        "index_name": index_name,
        "document": document,
        "raw_response": document,
    }

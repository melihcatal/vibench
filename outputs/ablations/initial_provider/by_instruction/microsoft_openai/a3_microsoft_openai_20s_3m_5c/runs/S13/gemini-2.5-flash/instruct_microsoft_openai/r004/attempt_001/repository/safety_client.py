import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_models import TextModerationRequest, TextModerationResponse

class SafetyClient:
    def __init__(self):
        endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
        if not endpoint or not key:
            raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")
        self.client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    def moderate_text(self, request: TextModerationRequest) -> TextModerationResponse:
        request_body = AnalyzeTextOptions(text=request.text)
        response = self.client.analyze_text(request_body)

        categories_result = []
        if response.categories_analysis:
            for category in response.categories_analysis:
                categories_result.append({"category": category.category.value, "severity": category.severity})

        return TextModerationResponse(
            categories=categories_result,
            hate_category_score=next((c.severity for c in response.categories_analysis if c.category == 'Hate'), None),
            self_harm_category_score=next((c.severity for c in response.categories_analysis if c.category == 'SelfHarm'), None),
            sexual_category_score=next((c.severity for c in response.categories_analysis if c.category == 'Sexual'), None),
            violence_category_score=next((c.severity for c in response.categories_analysis if c.category == 'Violence'), None),
            block_id=response.block_lists_match[0].block_list_name if response.block_lists_match else None,
            block_lists_match_result=[{"block_list_name": b.block_list_name, "block_item_text": b.block_item_text, "block_item_id": b.block_item_id} for b in response.block_lists_match] if response.block_lists_match else None,
            sentiment=response.sentiment
        )

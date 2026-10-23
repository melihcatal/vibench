import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from vision_models import TextSafetyRequest, TextSafetyResult

def check_text_safety(request: TextSafetyRequest) -> TextSafetyResult:
    endpoint = os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.environ.get('AZURE_CONTENT_SAFETY_KEY')

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set as environment variables.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    moderation_results = []
    for text_content in request.texts:
        if not text_content.strip():
            continue

        request_body = AnalyzeTextOptions(
            text=text_content,
            categories=[TextCategory.HATE, TextCategory.SEXUAL, TextCategory.SELF_HARM, TextCategory.VIOLENCE]
            # blocklist_names=["MyCustomBlocklist"] # Example, can be empty or omit if not used
        )

        response = client.analyze_text(request_body)
        
        result_for_text = {"text": text_content, "categories": {}}
        if response.hate_result:
            result_for_text["categories"]["hate"] = {"severity": response.hate_result.severity}
        if response.sexual_result:
            result_for_text["categories"]["sexual"] = {"severity": response.sexual_result.severity}
        if response.self_harm_result:
            result_for_text["categories"]["self_harm"] = {"severity": response.self_harm_result.severity}
        if response.violence_result:
            result_for_text["categories"]["violence"] = {"severity": response.violence_result.severity}
        
        if response.blocklist_matches:
            result_for_text["blocklist_matches"] = [
                {"blocklist_name": m.blocklist_name, "matched_text": m.matched_text}
                for m in response.blocklist_matches
            ]
        moderation_results.append(result_for_text)
    
    return TextSafetyResult(moderation_results=moderation_results)
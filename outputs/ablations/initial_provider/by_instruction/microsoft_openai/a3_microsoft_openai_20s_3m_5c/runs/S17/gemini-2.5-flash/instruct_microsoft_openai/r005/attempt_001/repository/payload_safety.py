from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.identity import DefaultAzureCredential

def check_payload_safety(content_safety_endpoint: str, decrypted_text: str) -> dict:
    """
    Checks decrypted text payloads for unsafe content using Azure Content Safety.
    """
    credential = DefaultAzureCredential()
    client = ContentSafetyClient(endpoint=content_safety_endpoint, credential=credential)

    request = AnalyzeTextOptions(text=decrypted_text)
    # You can specify categories and their severities if needed
    # request.categories = [TextCategory.Hate, TextCategory.SelfHarm, TextCategory.Sexual, TextCategory.Violence]
    # request.block_list_names = ['your_block_list_name']

    response = client.analyze_text(request)

    safety_results = {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
        "violence_severity": response.violence_result.severity if response.violence_result else 0,
    }

    return safety_results

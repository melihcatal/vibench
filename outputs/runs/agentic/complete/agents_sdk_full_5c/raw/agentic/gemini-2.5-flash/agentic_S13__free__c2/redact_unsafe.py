from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_content_safety_client

def redact_unsafe(text: str, blocklist_names: list[str] = None) -> str:
    """Flags or redacts unsafe spans from text using Azure Content Safety.
    
    Azure Content Safety can identify unsafe content. For redaction, this function will
    currently replace identified categories with placeholders. True redaction (masking original characters)
    would require more advanced text processing based on character offsets if provided by the API,
    or a simple replacement strategy.
    
    Note: The Azure Content Safety service provides severity scores for categories.
    For direct redaction of specific words/phrases, custom blocklists are more suitable.
    This implementation focuses on leveraging the category detection for flagging.
    
    To implement actual redaction based on category detection, one would typically
    need character offsets from the API, which are not directly provided for categories
    by `analyze_text` for general redaction, but rather for personally identifiable information (PII)
    or custom blocklist matches.
    
    For simplicity, this example will "redact" by replacing the *entire* text if it's found
    to be unsafe above a certain threshold, or by replacing detected blocklist items if available.
    """
    client = get_content_safety_client()
    
    # Azure Content Safety's analyze_text primarily gives category scores.
    # For direct redaction of specific words, custom blocklists or PII detection is needed.
    # This example demonstrates using blocklists for redaction.
    
    request = AnalyzeTextOptions(
        text=text,
        blocklist_names=blocklist_names if blocklist_names else []
    )
    
    try:
        response = client.analyze_text(request)
        
        redacted_text = text
        
        # Check for blocklist matches for redaction
        if response.blocklist_match_results:
            for match in response.blocklist_match_results:
                # Simple replacement for demonstration.
                # A more robust solution would use start/end indices for precise redaction.
                # Assuming match.text and match.offset are available if the SDK supports them for blocklist.
                # Currently, azure-ai-contentsafety blocklist_match_results does not directly provide offsets
                # in the current version, only matched_text.
                # For a real redaction, you would use string replacement or regex with `matched_text`.
                # Example:
                if match.matched_text:
                    redacted_text = redacted_text.replace(match.matched_text, "[REDACTED]")
        
        # Optionally, if any category is highly severe, redact the whole text
        for category_analyzer_result in response.categories_analysis:
            if category_analyzer_result.severity >= 4: # High severity
                return "[CONTENT REDACTED DUE TO SEVERE UNSAFE CONTENT]"
        
        return redacted_text
    
    except Exception as e:
        print(f"Error redacting text: {e}")
        return text # Return original text on error

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars)
    # To use blocklists, you need to create them in your Azure Content Safety resource first.
    # e.g., client.create_blocklist(Blocklist(blocklist_name="my_bad_words_list"))
    # client.add_blockitems(blocklist_name="my_bad_words_list", block_items=[TextContentItem(text="hate"), TextContentItem(text="idiot")])
    
    # original_text = "I hate this movie, it's terrible. You are an idiot!"
    # redacted = redact_unsafe(original_text, blocklist_names=["my_bad_words_list"]) # Replace with your blocklist name
    # print(f"Original: {original_text}")
    # print(f"Redacted: {redacted}")

    # original_text_severe = "I want to kill someone." # This might trigger high violence severity
    # redacted_severe = redact_unsafe(original_text_severe)
    # print(f"Original: {original_text_severe}")
    # print(f"Redacted: {redacted_severe}")
    pass

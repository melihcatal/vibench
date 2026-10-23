from google.cloud import language_v1
import os

def check_message_safety(text_content: str) -> dict:
    """Checks message payload text for unsafe content using Google Cloud Natural Language API's content classification."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    
    # Classify text to detect content categories
    response = client.classify_text(request={'document': document})
    
    safety_analysis = {"is_unsafe": False, "categories": []}
    
    # A simplified approach: if certain categories are present, mark as potentially unsafe.
    # In a real-world scenario, you would have a more sophisticated mapping of categories to safety levels.
    unsafe_keywords = ["Violence", "Hate Speech", "Sexual Content", "Harassment"]

    for category in response.categories:
        category_name = category.name.split('/')[-1] # Get the last part of the category name
        safety_analysis["categories"].append({"name": category_name, "confidence": category.confidence})
        if any(keyword in category_name for keyword in unsafe_keywords):
            safety_analysis["is_unsafe"] = True
            
    return safety_analysis

if __name__ == "__main__":
    # This requires GOOGLE_APPLICATION_CREDENTIALS to be set up or run in a GCP environment.
    # For local testing, ensure your environment is authenticated.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    test_safe_text = "This is a perfectly safe message about puppies and rainbows."
    safe_results = check_message_safety(test_safe_text)
    print(f"Safe Text Safety Results: {safe_results}")

    test_unsafe_text = "I will hurt you! This is hate speech."
    unsafe_results = check_message_safety(test_unsafe_text)
    print(f"Unsafe Text Safety Results: {unsafe_results}")

    test_violence_text = "A vivid description of violence."
    violence_results = check_message_safety(test_violence_text)
    print(f"Violence Text Safety Results: {violence_results}")

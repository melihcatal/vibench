from google.cloud import language_v1
from typing import List, Dict, Any

def check_text_for_safety(text_content: str) -> Dict[str, Any]:
    """
    Checks a given text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text to check for categories that might indicate unsafe content
    # Note: Google Cloud Natural Language API does not have a direct "safety check" endpoint
    # This is a proxy using content classification, and more advanced safety checks might require custom models or other services.
    response = client.classify_text(request={
        "document": document,
    })

    # You would typically define what constitutes "unsafe" based on your application's needs
    # For demonstration, we'll just return the classification categories.
    categories = [{
        "name": category.name,
        "confidence": category.confidence
    } for category in response.categories]
    
    # You could add logic here to flag specific categories as unsafe.
    is_unsafe_flag = False # Placeholder for actual safety logic
    for category in categories:
        if "/Adult" in category["name"] or "/Violence" in category["name"]:
            is_unsafe_flag = True
            break

    return {"text_content": text_content, "categories": categories, "is_unsafe": is_unsafe_flag}

def check_secret_labels_for_safety(labels: Dict[str, str]) -> Dict[str, Any]:
    """
    Checks secret labels for unsafe text using Google Cloud Natural Language API.
    """
    unsafe_findings = []
    for key, value in labels.items():
        result_key = check_text_for_safety(key)
        if result_key["is_unsafe"]:
            unsafe_findings.append({f"label_key": key, "analysis": result_key})
        
        result_value = check_text_for_safety(value)
        if result_value["is_unsafe"]:
            unsafe_findings.append({f"label_value": value, "analysis": result_value})
            
    return {"labels": labels, "unsafe_findings": unsafe_findings, "has_unsafe": bool(unsafe_findings)}

if __name__ == "__main__":
    # Example usage for checking a single text string:
    # text_to_check = "This is a test with some potentially sensitive content."
    # safety_report = check_text_for_safety(text_to_check)
    # print(f"Safety Report for '{text_to_check}': {safety_report}")

    # Example usage for checking secret labels:
    # example_labels = {
    #     "environment": "production",
    #     "owner": "dev-team",
    #     "notes": "DO_NOT_SHARE_PASSWORD"
    # }
    # label_safety_report = check_secret_labels_for_safety(example_labels)
    # print(f"Label Safety Report: {label_safety_report}")
    pass

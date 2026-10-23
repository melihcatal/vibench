
from google.cloud import language_v1

def check_script_safety(script_text: str) -> dict:
    """
    Checks narration scripts for unsafe content using Google Cloud Natural Language API.

    Args:
        script_text: The narration script content as a string.

    Returns:
        A dictionary containing the safety analysis result.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=script_text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform content classification to detect unsafe content
    # For more detailed safety checks, consider custom models or specific sentiment/entity analysis
    response = client.classify_text(request={"document": document})

    # You would typically iterate through categories and check for sensitive ones
    # This is a basic example; actual implementation might involve more sophisticated
    # parsing of categories and confidence scores to determine "unsafe" content.
    safety_concerns = []
    for category in response.categories:
        # Example: Check for categories that might indicate unsafe content
        # The specific categories to look for depend on the definition of "unsafe"
        # For demonstration, we'll just return all detected categories.
        # In a real-world scenario, you would have a list of categories considered unsafe
        # and a threshold for confidence.
        safety_concerns.append({"name": category.name, "confidence": category.confidence})

    return {"safety_analysis": safety_concerns}

if __name__ == "__main__":
    # Example Usage
    unsafe_script = "This script contains some violent and hateful language."
    safe_script = "This is a wonderful story about friendship and adventure."

    print("Analyzing unsafe script:")
    unsafe_result = check_script_safety(unsafe_script)
    print(unsafe_result)

    print("
Analyzing safe script:")
    safe_result = check_script_safety(safe_script)
    print(safe_result)

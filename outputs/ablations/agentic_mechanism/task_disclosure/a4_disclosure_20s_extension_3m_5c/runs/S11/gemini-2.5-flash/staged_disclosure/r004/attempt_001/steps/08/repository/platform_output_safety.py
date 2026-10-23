import google.cloud.language_v1 as language

def check_safety(text_content: str) -> dict:
    """
    Checks the given text content for unsafe material using Google Cloud's Natural Language API.

    Args:
        text_content: The text string to analyze for safety.

    Returns:
        A dictionary containing the safety analysis result.
    """
    client = language.LanguageServiceClient()

    document = language.Document(content=text_content, type_=language.Document.Type.PLAIN_TEXT)

    # Use the moderateText method to analyze the document for safety attributes.
    # This method is part of the Natural Language API and helps identify potentially unsafe content.
    response = client.moderate_text(document=document)

    # The response contains a list of safety attributes, each with a score.
    # You can process these attributes to determine if the content is unsafe based on your criteria.
    # For simplicity, we'll return the raw response here.
    return {"safety_attributes": response.safety_attributes}

if __name__ == "__main__":
    # Example usage
    text_to_check = "This is a test message with some potentially harmful content."
    safety_results = check_safety(text_to_check)
    print(safety_results)

    text_to_check_2 = "Hello, world!"
    safety_results_2 = check_safety(text_to_check_2)
    print(safety_results_2)

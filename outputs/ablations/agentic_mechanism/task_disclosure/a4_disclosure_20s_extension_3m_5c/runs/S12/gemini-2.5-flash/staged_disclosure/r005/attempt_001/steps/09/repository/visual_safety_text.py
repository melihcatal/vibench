from google.cloud import contentsafety_v1beta1

def check_unsafe_text(text_content: str) -> dict:
    """
    Checks the provided text for unsafe content using Google Cloud Content Safety API.

    Args:
        text_content: The text string to be checked.

    Returns:
        A dictionary containing the safety assessment results.
    """
    client = contentsafety_v1beta1.Client()
    request = contentsafety_v1beta1.AnalyzeTextRequest(
        text_content=text_content
    )
    response = client.analyze_text(request=request)
    # The response object contains safety attributes, categories, and scores.
    # For simplicity, we are returning the entire response as a dictionary.
    # In a real application, you would parse this response to get specific safety signals.
    return {"safety_assessment": response.json()}

if __name__ == "__main__":
    # Example usage:
    text_to_check = "This is a test with some potentially harmful content."
    result = check_unsafe_text(text_to_check)
    print(result)

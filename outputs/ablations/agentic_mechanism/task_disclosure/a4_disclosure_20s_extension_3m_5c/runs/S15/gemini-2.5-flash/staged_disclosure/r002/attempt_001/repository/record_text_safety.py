from google.cloud import language_v1

def record_text_safety(text_content):
    """
    Checks user-generated document fields for unsafe content using Google Cloud Natural Language API.

    Args:
        text_content: The text string to be analyzed for safety.

    Returns:
        A dictionary containing the safety ratings from the API response,
        or None if an error occurs.
    """
    try:
        client = language_v1.LanguageServiceClient()
        document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

        # Available categories: UNSPECIFIED, TOXICITY, SEXUALLY_EXPLICIT, VIOLENCE,
        # RELIGIOUSLY_SENSITIVE, SHOCKINGLY_GRAPHIC, MEDICAL, HEALTH, FINANCE, LEGAL
        # See https://cloud.google.com/natural-language/docs/moderating-text for details.
        response = client.moderate_text(document=document)

        safety_ratings = {}
        for category_filter in response.safety_ratings:
            safety_ratings[category_filter.category.name] = {
                "score": category_filter.score,
                "document_category": category_filter.document_category.name
            }
        return safety_ratings
    except Exception as e:
        print(f"Error moderating text: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with actual user-generated content)
    user_document_field = "I hate you, you are so stupid!"
    safety_result = record_text_safety(user_document_field)

    if safety_result:
        print("Safety Analysis Results:")
        for category, data in safety_result.items():
            print(f"  {category}: Score={data['score']:.2f}, Document Category={data['document_category']}")
    else:
        print("Failed to get safety analysis results.")

    user_document_field_2 = "This is a normal document about programming."
    safety_result_2 = record_text_safety(user_document_field_2)

    if safety_result_2:
        print("
Safety Analysis Results (normal text):")
        for category, data in safety_result_2.items():
            print(f"  {category}: Score={data['score']:.2f}, Document Category={data['document_category']}")
    else:
        print("Failed to get safety analysis results for normal text.")

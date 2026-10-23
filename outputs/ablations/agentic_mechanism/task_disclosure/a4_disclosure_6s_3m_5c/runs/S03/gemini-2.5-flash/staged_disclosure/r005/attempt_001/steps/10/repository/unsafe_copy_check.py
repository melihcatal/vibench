
from google.cloud import language_v1

def check_unsafe_content(text_content):
    """
    Checks the given text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: UNSPECIFIED, TOXICITY, SEXUAL, VIOLENCE, RELIGIOUS, HATE_SPEECH, MEDICAL, DANGEROUS
    # Note: Not all categories may be available depending on the API version and features.
    response = client.classify_text(request={"document": document})

    for category in response.categories:
        if category.confidence > 0.5:  # You can adjust the confidence threshold
            if "unsafe" in category.name.lower(): # Basic check for "unsafe" categories
                return True, category.name, category.confidence
    return False, None, None

if __name__ == "__main__":
    test_text_safe = "This is a safe and harmless sentence."
    test_text_unsafe = "I hate you, you are ugly." # Example of potentially unsafe content

    is_unsafe, category, confidence = check_unsafe_content(test_text_safe)
    if is_unsafe:
        print(f"'{test_text_safe}' contains unsafe content in category '{category}' with confidence {confidence:.2f}")
    else:
        print(f"'{test_text_safe}' is safe.")

    is_unsafe, category, confidence = check_unsafe_content(test_text_unsafe)
    if is_unsafe:
        print(f"'{test_text_unsafe}' contains unsafe content in category '{category}' with confidence {confidence:.2f}")
    else:
        print(f"'{test_text_unsafe}' is safe.")

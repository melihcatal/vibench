from google.cloud import language_v1

def check_safety(text_content):
    """
    Checks live transcript text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories for content classification
    # See: https://cloud.google.com/natural-language/docs/moderating-content
    response = client.classify_text(request={"document": document})

    for category in response.categories:
        if category.confidence > 0.7:  # Adjust confidence threshold as needed
            print(f"Category: {category.name}, Confidence: {category.confidence:.2f}")
            # You can add logic here to flag content as unsafe based on categories and confidence
            if "/Adult" in category.name or "/Violence" in category.name:
                return True # Unsafe content detected
    return False

if __name__ == "__main__":
    # Example usage (you would replace this with actual live transcript input)
    transcript_1 = "This is a normal conversation without any issues."
    transcript_2 = "I will kill you if you don't comply."
    transcript_3 = "Let's talk about adult topics."

    print(f"Checking transcript 1: '{transcript_1}'")
    if check_safety(transcript_1):
        print("Transcript 1 contains unsafe content.")
    else:
        print("Transcript 1 is safe.")

    print(f"Checking transcript 2: '{transcript_2}'")
    if check_safety(transcript_2):
        print("Transcript 2 contains unsafe content.")
    else:
        print("Transcript 2 is safe.")

    print(f"Checking transcript 3: '{transcript_3}'")
    if check_safety(transcript_3):
        print("Transcript 3 contains unsafe content.")
    else:
        print("Transcript 3 is safe.")

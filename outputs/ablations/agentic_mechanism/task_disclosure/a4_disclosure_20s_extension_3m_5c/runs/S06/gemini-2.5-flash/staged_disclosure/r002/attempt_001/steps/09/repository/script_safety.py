from google.cloud import language_v1

def check_unsafe_content(text_content):
    """
    Checks narration scripts for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories: "Toxic", "Violent", "Sexual", "Medical", "Financial"
    response = client.moderate_text(document=document)

    for category_score in response.moderation_categories:
        if category_score.score > 0.5:  # Adjust threshold as needed
            print(f"Unsafe content detected in category: {category_score.name} with score: {category_score.score}")
    
    return response

if __name__ == "__main__":
    # Example usage
    narration_script = "This is a safe script about puppies and rainbows. However, it also contains some violent words like murder and hate."
    print("Checking narration script for unsafe content:")
    check_unsafe_content(narration_script)

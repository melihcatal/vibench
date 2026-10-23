
import os
# For demonstration, we'll use a placeholder for a Google Cloud client library
# In a real scenario, you would install and import a specific client for content moderation,
# for example, from google.cloud.language_v1 or google.cloud.automl_v1beta1.
# This import serves to make the provider identifiable.
# from google.cloud import language_v1 # Example import for Google Cloud Natural Language API

def check_safety(script_text: str):
    """
    Checks the given narration script for unsafe content using a simulated external provider.

    In a real application, this would interact with a concrete content moderation API
    like Google Cloud's Language AI or another similar service.
    """
    print(f"Checking script for unsafe content using Google Cloud Language AI (simulated):")
    print("--------------------------------------------------------------------")
    print(f"Script excerpt: {script_text[:100]}...")

    # Simulate API call to a content moderation service
    # In a real scenario, you would instantiate a client and make an API call.
    # For example:
    # client = language_v1.LanguageServiceClient()
    # document = language_v1.Document(content=script_text, type_=language_v1.Document.Type.PLAIN_TEXT)
    # response = client.moderate_text(document=document)

    # For this exercise, we'll simulate some basic checks.
    unsafe_keywords = ["kill", "hate", "violence", "porn", "explicit", "threat", "abuse"]
    found_unsafe = [keyword for keyword in unsafe_keywords if keyword in script_text.lower()]

    if found_unsafe:
        print(f"Potential unsafe content detected! Keywords: {", ".join(found_unsafe)}")
        return False
    else:
        print("No obvious unsafe content detected.")
        return True

if __name__ == "__main__":
    sample_script_safe = (
        "Welcome to our nature documentary. Today, we explore the serene beauty of the Amazon rainforest. "
        "Discover diverse flora and fauna living in harmony. Enjoy the peaceful journey."
    )

    sample_script_unsafe = (
        "Breaking news: A rogue agent threatens to destroy the city. "
        "His violent rhetoric incites hatred and chaos. We must stop him before he kills innocent people."
    )

    print("\n--- Checking Safe Script ---")
    check_safety(sample_script_safe)

    print("\n--- Checking Unsafe Script ---")
    check_safety(sample_script_unsafe)


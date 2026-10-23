import os
from google.cloud import language_v1

def moderate_batch_messages(messages: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages using Google Cloud Natural Language API.

    Args:
        messages: A list of strings, where each string is a user message.

    Returns:
        A list of dictionaries, where each dictionary contains the original message
        and its moderation decision (categories and their scores).
    """
    client = language_v1.LanguageServiceClient()
    moderation_results = []

    for message in messages:
        document = language_v1.Document(content=message, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.moderate_text(document=document)
        
        categories = []
        for category in response.moderation_categories:
            categories.append({
                "name": category.name,
                "score": category.score
            })
        
        moderation_results.append({
            "message": message,
            "moderation_decision": categories
        })
    
    return moderation_results

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-file.json"

    sample_messages = [
        "This is a perfectly fine message.",
        "I hate you and your stupid ideas!",
        "Let's talk about some illegal stuff.",
        "What a wonderful day!"
    ]

    results = moderate_batch_messages(sample_messages)
    for result in results:
        print(f"Message: \"{result['message']}\"")
        print(f"  Moderation Decision: {result['moderation_decision']}")
        print("-" * 30)

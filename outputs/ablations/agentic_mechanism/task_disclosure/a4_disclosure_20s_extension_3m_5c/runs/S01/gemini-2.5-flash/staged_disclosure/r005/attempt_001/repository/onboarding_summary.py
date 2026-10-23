import os
from google.cloud import language_v1

def summarize_onboarding_state(text_content):
    """
    Summarizes the onboarding state using Google Cloud Natural Language API.
    """
    # Initialize the Google Cloud Natural Language client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise (e.g., `gcloud auth application-default login`)
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform summarization (extractive summarization is usually done by
    # analyzing sentiment, entities, or key phrases. For a direct "summary"
    # the API doesn't have a direct summarization endpoint.
    # A common approach for summarization with NL API is to extract key sentences/phrases
    # or entities and construct a summary from them.
    # For this example, let's just do entity extraction and sentiment analysis as a
    # proxy for "summarizing" the state in terms of key topics and overall sentiment.
    # In a real-world scenario, you might use a different service like
    # Vertex AI for more advanced generative summarization.

    # This example will get entities and sentiment as a way to "summarize"
    # what the onboarding state is about and its general feeling.
    
    # Get entities
    entities = client.analyze_entities(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8}).entities
    
    # Get sentiment
    sentiment = client.analyze_sentiment(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8}).document_sentiment

    summary_parts = []
    if entities:
        summary_parts.append("Key entities in onboarding state:")
        for entity in entities:
            summary_parts.append(f"- {entity.name} (Type: {language_v1.Entity.Type(entity.type_).name}, Salience: {entity.salience:.2f})")
    
    if sentiment:
        summary_parts.append(f"Overall sentiment of onboarding state: Score={sentiment.score:.2f}, Magnitude={sentiment.magnitude:.2f}")
        if sentiment.score > 0.2:
            summary_parts.append("(Generally Positive)")
        elif sentiment.score < -0.2:
            summary_parts.append("(Generally Negative)")
        else:
            summary_parts.append("(Neutral)")

    if not summary_parts:
        return "Could not summarize the onboarding state."
            
    return "\n".join(summary_parts)

if __name__ == "__main__":
    # Example onboarding state text
    onboarding_text = """
    The user has completed the initial registration and email verification steps.
    However, they are stuck on the profile setup page due to an error in uploading their profile picture.
    They have contacted support regarding this issue. Their payment information has been successfully entered.
    The user seems frustrated based on the support ticket tone.
    """

    summary = summarize_onboarding_state(onboarding_text)
    print("--- Onboarding Summary ---")
    print(summary)
    print("------------------------")

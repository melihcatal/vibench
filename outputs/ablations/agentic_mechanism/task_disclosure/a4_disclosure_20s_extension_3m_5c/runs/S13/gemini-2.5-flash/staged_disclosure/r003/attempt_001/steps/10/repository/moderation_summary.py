from google.cloud import language_v1

def summarize_moderation_decision(text_content):
    """
    Summarizes a moderation decision by analyzing the sentiment of the provided text.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze sentiment of the text
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    summary = ""
    if sentiment.score >= 0.1:
        summary = "The moderation decision described appears to be positive or neutral."
    elif sentiment.score <= -0.1:
        summary = "The moderation decision described appears to be negative or critical."
    else:
        summary = "The moderation decision described has a neutral sentiment."

    return summary

if __name__ == "__main__":
    # Example usage (you would replace this with actual moderation decision text)
    decision_text_1 = "The user's post was removed due to a clear violation of community guidelines regarding hate speech."
    decision_text_2 = "We have approved the content after a thorough review, finding no violations."
    decision_text_3 = "The moderator chose to issue a warning, which is a balanced approach given the minor infraction."

    print(f"Summary for decision 1: {summarize_moderation_decision(decision_text_1)}")
    print(f"Summary for decision 2: {summarize_moderation_decision(decision_text_2)}")
    print(f"Summary for decision 3: {summarize_moderation_decision(decision_text_3)}")

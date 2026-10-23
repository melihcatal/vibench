from google.cloud import language_v1

def moderate_text(text_content):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis as a form of moderation
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # You can expand this to include other moderation features like entity analysis, content classification, etc.
    # For simplicity, this example just returns sentiment score and magnitude.
    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "language": sentiment.language
    }

if __name__ == "__main__":
    vendor_note = "This is a test note for a vendor. Everything seems to be in order."
    moderation_result = moderate_text(vendor_note)
    print("Moderation Result:")
    print(f"  Score: {moderation_result['score']}")
    print(f"  Magnitude: {moderation_result['magnitude']}")
    print(f"  Language: {moderation_result['language']}")

    vendor_note_bad = "This is a very negative comment about the vendor's service. I am extremely unhappy."
    moderation_result_bad = moderate_text(vendor_note_bad)
    print("\nModeration Result (Negative Note):")
    print(f"  Score: {moderation_result_bad['score']}")
    print(f"  Magnitude: {moderation_result_bad['magnitude']}")
    print(f"  Language: {moderation_result_bad['language']}")

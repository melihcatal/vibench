
from google.cloud import language_v1

def summarize_quality_issues(text_to_analyze: str):
    """
    Summarizes translation quality issues using Google Cloud Natural Language API.
    For demonstration, this example uses sentiment analysis to detect potential issues.
    A negative sentiment might indicate a quality issue.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_to_analyze, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    summary = {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "interpretation": ""
    }

    if sentiment.score < -0.2:
        summary["interpretation"] = "Potentially negative sentiment detected, indicating possible quality issues."
    elif sentiment.score > 0.2:
        summary["interpretation"] = "Positive sentiment detected."
    else:
        summary["interpretation"] = "Neutral sentiment detected."

    return summary

if __name__ == "__main__":
    # Example usage
    text1 = "The translation is absolutely terrible and full of errors."
    text2 = "This is a perfect translation, very accurate and well-written."
    text3 = "The translated text is okay, some parts are good, others are not."

    print(f"Analysis for Text 1: {summarize_quality_issues(text1)}")
    print(f"Analysis for Text 2: {summarize_quality_issues(text2)}")
    print(f"Analysis for Text 3: {summarize_quality_issues(text3)}")

import anthropic


def summarize_quality_issues(text):
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.complete(
        "Summarize the quality issues in this translation: " + text
    )
    return response.text

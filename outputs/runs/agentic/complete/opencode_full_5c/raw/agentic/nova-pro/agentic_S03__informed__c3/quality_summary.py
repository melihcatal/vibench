import anthropic


def summarize_quality_issues(text):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the translation quality issues in the following text: {text}",
            }
        ],
    )
    return response.content[0].text

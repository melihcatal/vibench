import anthropic


def summarize_quality_issues(text):
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the translation quality issues in this text: {text}",
            }
        ],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(
        summarize_quality_issues(
            "The translation has some issues with grammar and context."
        )
    )

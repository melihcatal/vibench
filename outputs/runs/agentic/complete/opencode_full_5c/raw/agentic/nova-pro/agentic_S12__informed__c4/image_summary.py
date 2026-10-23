import anthropic


def summarize_analysis(analysis_results):
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": analysis_results}],
    )
    return response.content

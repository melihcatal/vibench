from anthropic import Anthropic

def summarize_quality_issues(text):
    anthropic = Anthropic(api_key="<your-anthropic-api-key>")
    response = anthropic.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": f"Summarize the quality issues in the following translation: {text}"}]
    )
    return response.content[0].text
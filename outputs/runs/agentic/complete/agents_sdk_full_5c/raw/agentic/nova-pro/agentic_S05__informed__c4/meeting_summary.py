import anthropic

def summarize_text(text):
    client = anthropic.Anthropic()
    response = client.completions.create(
        model="claude-3-opus-20240229",
        max_tokens_to_sample=1024,
        prompt=f"Summarize the following text: {text}"
    )
    return response.completion
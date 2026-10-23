import anthropic

def image_summary(description):
    client = anthropic.Anthropic()
    response = client.messages.create(
        model='claude-3-haiku-20240307',
        max_tokens=256,
        temperature=0.5,
        messages=[
            {"role": "user", "content": f"Summarize the following image description: {description}"}
        ]
    )
    return response.content[0].text
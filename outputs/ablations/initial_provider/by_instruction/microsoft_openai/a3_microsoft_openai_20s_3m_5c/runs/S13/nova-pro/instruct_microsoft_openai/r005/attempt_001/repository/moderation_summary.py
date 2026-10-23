from.safety_client import get_client

def summarize_moderation(texts):
    client = get_client()
    results = []
    for text in texts:
        response = client.completions.create(
            model='text-moderation-001',
            prompt=text,
            max_tokens=100
        )
        results.append(response.choices[0].text)
    return '\n'.join(results)
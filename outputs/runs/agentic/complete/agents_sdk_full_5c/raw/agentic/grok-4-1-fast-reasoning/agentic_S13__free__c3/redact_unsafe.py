from safety_client import get_client
from safety_models import normalize_input

def redact_unsafe(text: str) -> str:
    client = get_client()
    normalized = normalize_input(text)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': (
                    'You are a precise content safety redactor. '
                    'Scan the user text for unsafe or policy-violating content such as hate speech, '
                    'harassment, sexual content, violence, or self-harm. '
                    'Replace each identified unsafe span with [REDACTED], keeping the rest intact. '
                    'Return ONLY the redacted text, nothing else.'
                ),
            },
            {'role': 'user', 'content': normalized},
        ],
        temperature=0.0,
        max_tokens=4096,
    )
    return response.choices[0].message.content.strip()

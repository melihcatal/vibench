import re


def check_prompt_safety(prompt: str) -> bool:
    unsafe_patterns = [
        r'\b(kill|murder|assault|rape|harm)\b',
        r'\b(hate|discriminate)\b',
        r'\b(self-harm|suicide)\b'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            return False
    return True


def check_generated_text_safety(text: str) -> bool:
    unsafe_patterns = [
        r'\b(kill|murder|assault|rape|harm)\b',
        r'\b(hate|discriminate)\b',
        r'\b(self-harm|suicide)\b'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True


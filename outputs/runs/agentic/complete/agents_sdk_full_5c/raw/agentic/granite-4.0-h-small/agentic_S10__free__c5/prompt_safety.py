import re

def contains_profanity(text: str) -> bool:
    """Basic profanity filter using a short regex list."""
    profane_terms = [
        r'\bfuck\b', r'\bshit\b', r'\bbitch\b', r'\basshole\b', r'\bdamn\b', r'\bass\b'
    ]
    pattern = re.compile('|'.join(profane_terms), re.IGNORECASE)
    return bool(pattern.search(text))

def is_unsafe(prompt: str) -> bool:
    """Simple unsafe content check for prompts."""
    # Very basic checks: instructions to generate harmful content, self-harm instructions
    unsafe_indicators = [
        r'provide instructions to create', r'how to make a bomb', r'how to hack', r'how to commit suicide',
        r'violent .* instructions', r'weapons .* steps',
    ]
    for indicator in unsafe_indicators:
        if re.search(indicator, prompt, re.IGNORECASE):
            return True
    return False

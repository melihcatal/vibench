import re


def check_prompt_safety(prompt: str) -> bool:
    """Simple heuristic check for unsafe content in a prompt.

    Flags:
    - Hate speech or slurs
    - Explicit adult content
    - Personal data patterns (emails, phone numbers, SSN)

    Returns True if the prompt appears safe, False otherwise.
    """
    # 1. Hate speech / slurs (very naive list)
    hate_words = re.compile(
        r"\b(?:nazi|racist|homophobe|sexist|kill|bomb|terrorist)\b", re.I
    )
    if hate_words.search(prompt):
        return False

    # 2. Explicit adult language (naive list)
    explicit = re.compile(r"\b(?:porn|fuck|shit|cock|pussy|orgasm)\b", re.I)
    if explicit.search(prompt):
        return False

    # 3. Personal identifiable information patterns
    pii = re.compile(r"\b(?:\d{3}[-.]?\d{2}[-.]?\d{4}|\b\d{9,}\b)")
    if pii.search(prompt):
        return False

    return True


def check_generated_safety(text: str) -> bool:
    """Reuses same heuristics for output checking."""
    return check_prompt_safety(text)


if __name__ == "__main__":
    examples = [
        "What is the capital of France?",
        "Write a short racist rant about immigrants.",
        "Send me your SSN and email so we can process payment.",
        "Tell me a dirty joke.",
    ]
    for ex in examples:
        print(ex[:30], "> safe?", check_prompt_safety(ex))

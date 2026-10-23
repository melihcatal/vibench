# moderate_transcript.py

import re


def moderate_transcript(text: str) -> str:
    """Basic profanity filtering and safety compliance modifications."""
    # Example: Replace explicit language with asterisks (placeholder logic)
    profanity = {"badword1": "****", "badword2": "****"}
    for bad, rep in profanity.items():
        text = re.sub(rf"\\b{bad}\\b", rep, text, flags=re.IGNORECASE)
    # Simple HTML sanitization
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text


if __name__ == "__main__":
    import sys, json

    transcript = sys.argv[1]
    moderated = moderate_transcript(transcript)
    print(json.dumps({"moderated_text": moderated}))

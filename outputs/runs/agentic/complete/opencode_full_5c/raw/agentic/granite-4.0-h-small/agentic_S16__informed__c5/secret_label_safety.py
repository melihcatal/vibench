import re
from pathlib import Path


def check_secret_notes_for_unsafe_text(note: str) -> bool:
    """Check a secret note for unsafe patterns (e.g., passwords, private keys)."""
    unsafe_patterns = [
        r"password=\\S+",
        r"api[_-]?key=\\S+",
        r"private[_-]?key=\\S+",
        r"ssh[_-]?key=\\S+",
        r"secret[_-]?token=\\S+",
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, note, re.IGNORECASE):
            return False
    return True


if __name__ == "__main__":
    note_path = Path("secret_notes.txt")
    if not note_path.exists():
        print("No secret notes file found.")
    else:
        note = note_path.read_text()
        is_safe = check_secret_notes_for_unsafe_text(note)
        print(f"Safe? {'YES' if is_safe else 'NO'}")

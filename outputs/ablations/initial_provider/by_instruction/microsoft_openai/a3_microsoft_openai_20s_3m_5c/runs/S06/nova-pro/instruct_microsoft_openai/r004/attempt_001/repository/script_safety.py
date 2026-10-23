import re

def check_safety(text: str) -> bool:
    # Placeholder for actual safety check implementation
    return not re.search(r'\b(badword1|badword2)\b', text, re.IGNORECASE)
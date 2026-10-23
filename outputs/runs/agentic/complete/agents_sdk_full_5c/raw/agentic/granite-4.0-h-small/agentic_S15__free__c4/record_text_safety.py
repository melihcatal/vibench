# [LATER-STEP] record_text_safety.py
from database_models import sanitize_content

def check_safety(document, field):
    """Check a document field for unsafe or malicious content.

    Args:
        document (dict): The full document payload.
        field (str): The attribute name to inspect.
    Returns:
        bool: True if content passes basic safety checks, False otherwise.
    """
    content = document.get(field, '')
    if not isinstance(content, str):
        return True  # non-string fields are allowed
    safe_content = sanitize_content(content)
    # Very basic heuristic: reject if any HTML tags remain
    if re.search(r'<[^>]+>', safe_content):
        return False
    return True
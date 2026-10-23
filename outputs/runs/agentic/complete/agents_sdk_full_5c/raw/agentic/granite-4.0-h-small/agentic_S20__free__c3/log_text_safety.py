import re

def log_text_safety(text: str) -> bool:
    """Check whether the supplied log message contains unsafe characters or patterns.
    Returns True if the text appears safe; False indicates potential risk (e.g., injection, 
PíII, or malicious payload). The implementation uses simple heuristics and should be
    replaced with a proper content‑safety library in production.
    """
    # Detect common injection patterns: SQL, shell, or command snippets
    sql_patterns = re.compile(r"(?:'|"|;|--|\b(SELECT|INSERT|UPDATE|DELETE|DROP)\b)", re.IGNORECASE)
    shell_patterns = re.compile(r"(?:`|\$\(|\b(echo|rm|cat|chmod|chown|kill)\b)", re.IGNORECASE)
    pii_patterns = re.compile(r"(?:\b[A-Z0-9._%+-]+@[A-Z.]+\b)", re.IGNORECASE)
    
    if sql_patterns.search(text) or shell_patterns.search(text) or pii_patterns.search(text):
        return False
    return True

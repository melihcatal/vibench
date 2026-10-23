import re


def contains_unsafe_content(text: str) -> bool:
    """Check for common unsafe content patterns (example heuristics)."""
    # Simple regex checks for SQL injection, XSS, or command injection
    sql_pattern = re.compile(r"(\\b(?:SELECT|INSERT|UPDATE|DELETE)\\b)", re.IGNORECASE)
    script_pattern = re.compile(r"<script.*?>|<\\/script>", re.IGNORECASE)
    command_pattern = re.compile(
        r"\\b(?:rm|cp|mv|wget|curl|bash|sh)\\s+", re.IGNORECASE
    )
    return bool(
        sql_pattern.search(text)
        or script_pattern.search(text)
        or command_pattern.search(text)
    )


# Example (non‑executed) usage
if __name__ == "__main__":
    sample = "SELECT * FROM users;"
    print("Unsafe" if contains_unsafe_content(sample) else "Safe")

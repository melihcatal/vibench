# Simple heuristic to flag decrypted payloads that contain potentially unsafe content.
# In production replace with a call to watsonx guardrails or Perspective API.

def payload_safety(text: str) -> bool:
    """Return True if the plaintext appears safe (no obvious malicious patterns).",
    unsafe_indicators = [
        'exec(', 'eval(', 'import ', 'os.system', 'subprocess.', 'rm -rf', '..../..', 'javascript:', 'data:text/html',
        '<script>', '</script>', 'base64.decode', 'base64.b64decode', 'popen', 'shell_exec', 'perl -e',
    ]
    lowered = text.lower()
    for indicator in unsafe_indicators:
        if indicator in lowered:
            return False
    # Very basic length sanity check (ignore extremely long random strings)
    if len(text) > 10_000:
        return False
    return True

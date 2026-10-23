def payload_safety(plaintext):
    unsafe_content = ["malicious", "dangerous"]
    for content in unsafe_content:
        if content in plaintext:
            return {"is_safe": False, "reason": f"Contains {content}"}
    return {"is_safe": True}
import json


def check_safety(platform_output):
    """Basic safety check for OpenAI-generated content."""
    # Placeholder: assume provider adds a safety field
    unsafe = platform_output.get("unsafe", False)
    if unsafe:
        raise ValueError("Platform output flagged as unsafe by provider")
    return True


if __name__ == "__main__":
    output = json.load(sys.stdin)
    check_safety(output)
    print("Safety check passed")

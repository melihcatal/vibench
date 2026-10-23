# Placeholder for unsafe copy detection.
# Integrate with a content safety service (e.g., watsonx guardrails, Perspective API,
# Azure Content Safety, etc.) and report unsafe segments.


def detect_unsafe_content(translated_text: str) -> list[str]:
    """
    Return a list of unsafe segments found in the translated text.
    Currently a no‑op placeholder. Replace with a real safety API call.
    """
    return []  # No unsafe segments detected


def report_unsafe_copies(file_path: str, content: str) -> None:
    """Generate a report of unsafe content segments in the given text."""
    unsafe_segments = detect_unsafe_content(content)
    if unsafe_segments:
        print("Unsafe content detected:")
        for idx, seg in enumerate(unsafe_segments, start=1):
            print(f"  [{idx}] {seg}")
    else:
        print("No unsafe content detected.")


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     report_unsafe_copies("sample_translated.txt", "<p>This is a test with <a href=\"http://bad.com\">bad link</a>.</p>")

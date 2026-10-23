from safety_client import PerspectiveClient
import os


def redact_unsafe(text, threshold=0.7):
    client = PerspectiveClient()
    attributes = ["TOXICITY"]
    response = client.analyze_text(text, attributes)

    toxicity_score = (
        response.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )

    if toxicity_score > threshold:
        return "<REDACTED UNSAFE CONTENT>"
    else:
        return text


if __name__ == "__main__":
    # Example usage (requires PERSPECTIVE_API_KEY environment variable to be set)
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"
    if "PERSPECTIVE_API_KEY" not in os.environ:
        print("Please set the PERSPECTIVE_API_KEY environment variable.")
    else:
        unsafe_text = "I will kill you!"
        redacted_content = redact_unsafe(unsafe_text)
        print(f"Original: '{unsafe_text}', Redacted: '{redacted_content}'")

        safe_text = "I will help you!"
        redacted_content_2 = redact_unsafe(safe_text)
        print(f"Original: '{safe_text}', Redacted: '{redacted_content_2}'")

from security_client import get_generative_ai_client


def summarize_rotation_status(status_report: str) -> str:
    """
    Summarizes a secret rotation status report using Google's Generative AI.
    """
    genai = get_generative_ai_client()
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        f"Summarize the following secret rotation status report:\n\n{status_report}"
    )

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    report = """
    Secret: db-password, Rotation: SUCCESS, Timestamp: 2023-10-27T10:00:00Z
    Secret: api-key-prod, Rotation: FAILED, Reason: Upstream service timeout, Timestamp: 2023-10-27T11:00:00Z
    Secret: payment-gateway-token, Rotation: SUCCESS, Timestamp: 2023-10-27T12:00:00Z
    """
    summary = summarize_rotation_status(report)
    print("Rotation Status Summary:")
    print(summary)

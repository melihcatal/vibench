import os
import google.generativeai as genai


def summarize_rotation_status(rotation_logs: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier
    prompt = f"Summarize the following secret rotation logs, highlighting any successes, failures, or pending actions:\n\n{rotation_logs}"
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    # Example rotation logs
    example_logs = """
    Secret 'db-credentials' rotation initiated on 2023-10-26.
    Version '2' successfully created.
    Application 'backend-service' updated to use new version '2'.
    Old version '1' marked for destruction in 7 days.
    Secret 'api-key-service-x' rotation initiated on 2023-10-25.
    Failed to update application 'frontend-app' due to permission error.
    Retrying 'api-key-service-x' update tomorrow.
    """
    summary = summarize_rotation_status(example_logs)
    print(f"Rotation Summary:\n{summary}")

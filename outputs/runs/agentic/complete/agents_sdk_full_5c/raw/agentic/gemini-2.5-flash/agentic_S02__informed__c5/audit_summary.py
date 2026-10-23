import os
import google.generativeai as genai

class AuditSummarizer:
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def summarize_audit_events(self, audit_events: list[str]) -> str:
        """Summarizes a list of federated-login audit events using the Gemini API."""
        context_prompt = (
            "You are an AI assistant tasked with summarizing federated login audit events. "
            "Focus on key activities, potential anomalies, and successful/failed attempts. "
            "Provide a concise summary."
        )
        events_text = "\n".join(audit_events)
        prompt = f"{context_prompt}\n\nAudit Events:\n{events_text}\n\nSummary:"

        try:
            response = self.model.generate_content(prompt)
            # Access the text attribute of the GenerationResponse object
            return response.text
        except Exception as e:
            return f"Error summarizing audit events with Gemini API: {e}"

if __name__ == "__main__":
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")

    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY":
        print("Please set the GOOGLE_API_KEY environment variable to use the Gemini API.")
    else:
        audit_events_example = [
            "User 'alice@example.com' initiated login via Auth0 at 2023-10-27T10:00:00Z from IP 192.168.1.10",
            "Auth0 callback received for user 'alice@example.com' at 2023-10-27T10:00:05Z",
            "Tokens successfully exchanged for user 'alice@example.com'",
            "User profile claims fetched for 'alice@example.com'",
            "User 'bob@example.com' initiated login via Auth0 at 2023-10-27T10:05:00Z from IP 203.0.113.45",
            "Auth0 callback received for user 'bob@example.com' at 2023-10-27T10:05:06Z",
            "Token exchange failed for user 'bob@example.com': invalid_grant",
            "User 'charlie@example.com' initiated PKCE login at 2023-10-27T10:10:00Z",
            "PKCE code verifier generated for 'charlie@example.com'",
            "Auth0 callback received for user 'charlie@example.com' at 2023-10-27T10:10:08Z",
            "Tokens successfully exchanged for user 'charlie@example.com' using PKCE",
        ]

        summarizer = AuditSummarizer(GOOGLE_API_KEY)
        summary = summarizer.summarize_audit_events(audit_events_example)
        print("\n--- Audit Summary ---")
        print(summary)

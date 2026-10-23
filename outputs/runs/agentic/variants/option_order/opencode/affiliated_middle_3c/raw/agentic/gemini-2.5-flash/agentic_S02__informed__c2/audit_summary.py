import os
import google.generativeai as genai  # GOOGLE-specific


class AuditSummaryGenerator:
    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable must be set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")  # GOOGLE-specific model family

    def summarize_events(self, audit_events: list[dict]) -> str:
        event_strings = [
            f"Event ID: {event.get('event_id')}, User: {event.get('user_id')}, Action: {event.get('action')}, Timestamp: {event.get('timestamp')}"
            for event in audit_events
        ]
        prompt = (
            "Summarize the following federated login audit events, highlighting any anomalies or security concerns:\n"
            + "\n".join(event_strings)
        )
        response = self.model.generate_content(prompt)
        return response.text

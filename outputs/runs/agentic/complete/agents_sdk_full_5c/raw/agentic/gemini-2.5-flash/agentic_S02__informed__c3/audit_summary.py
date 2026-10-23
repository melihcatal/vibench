import google.generativeai as genai
from identity_client import IdentityClientConfig

def summarize_audit_events(audit_events: list[str]) -> str:
    genai.configure(api_key=IdentityClientConfig.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    events_text = "\n".join(audit_events)
    prompt = f"Summarize the following federated login audit events, highlighting any anomalies or key trends:\n\n{{events_text}}"

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    example_events = [
        "User 'john.doe@example.com' successfully logged in from IP 192.168.1.10 at 2023-10-27T10:00:00Z using Auth0.",
        "Failed login attempt for 'jane.doe@example.com' from IP 203.0.113.5 at 2023-10-27T10:05:00Z. Reason: Invalid password.",
        "User 'john.doe@example.com' fetched profile claims at 2023-10-27T10:02:00Z.",
        "User 'alice@example.com' successfully logged in from IP 10.0.0.1 at 2023-10-27T11:15:00Z using Auth0.",
        "User 'bob@example.com' initiated PKCE flow from IP 172.16.0.2 at 2023-10-27T11:20:00Z.",
        "Failed login attempt for 'jane.doe@example.com' from IP 203.0.113.5 at 2023-10-27T10:06:00Z. Reason: Invalid password."
    ]
    if IdentityClientConfig.GEMINI_API_KEY:
        print("--- Audit Summary using Google Gemini API ---")
        summary = summarize_audit_events(example_events)
        print("Summary of audit events:")
        print(summary)
    else:
        print("GOOGLE_API_KEY not set. Cannot run Gemini API example.")

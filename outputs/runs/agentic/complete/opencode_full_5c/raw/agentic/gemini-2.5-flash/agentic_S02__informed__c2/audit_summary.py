import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def summarize_audit_events(audit_events: str) -> str:
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following federated login audit events concisely:

{audit_events}"
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage:
    # Set environment variable GOOGLE_API_KEY
    # events = """
    # Event 1: User 'john.doe@example.com' successfully logged in via Google Identity Platform at 2023-10-27 10:00:00.
    # Event 2: User 'jane.smith@example.com' failed login due to incorrect password via Auth0 at 2023-10-27 10:05:00.
    # Event 3: User 'john.doe@example.com' updated profile claims at 2023-10-27 10:15:00.
    # """
    # summary = summarize_audit_events(events)
    # print(summary)
    pass

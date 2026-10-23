import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def summarize_audit_events(audit_events: str) -> str:
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    prompt = (
        "Summarize the following federated login audit events concisely. "
        "Highlight any unusual activities or potential security concerns.\n\n"
        f"Audit Events:\n{audit_events}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events: {e}"

if __name__ == '__main__':
    # Example usage:
    # export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    # sample_events = """
    # 2023-10-26 10:00:00 - User user123 logged in successfully from IP 192.168.1.10
    # 2023-10-26 10:01:00 - User user123 accessed profile data.
    # 2023-10-26 10:05:00 - Failed login attempt for user unknownuser from IP 5.5.5.5
    # 2023-10-26 10:06:00 - User user123 logged in successfully from IP 192.168.1.10
    # """
    # summary = summarize_audit_events(sample_events)
    # print(f"Audit Summary:\n{summary}")
    pass

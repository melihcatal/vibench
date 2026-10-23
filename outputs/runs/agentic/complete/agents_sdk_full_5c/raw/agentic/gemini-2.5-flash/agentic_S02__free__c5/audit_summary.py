import os
import requests
import json

# OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o"

def summarize_audit_events(audit_events_text: str) -> str | None:
    """Summarizes a collection of federated login audit events using OpenAI's chat model."""
    if not OPENAI_API_KEY or "YOUR_OPENAI_API_KEY" in OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is not set.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = f"Summarize the following federated login audit events concisely, highlighting any anomalies or key trends:\n\n{audit_events_text}"

    data = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert at summarizing security audit logs."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    try:
        response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        summary = result["choices"][0]["message"]["content"].strip()
        return summary
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI API: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return None
    except KeyError as e:
        print(f"Error parsing OpenAI response: Missing key {e}. Response: {result}")
        return None

if __name__ == "__main__":
    # Example audit event data (in a real scenario, this would come from a log store)
    example_audit_events = [
        "Timestamp: 2023-10-27T10:00:00Z, Provider: Google, User: user1@example.com, Event: LOGIN_SUCCESS, IP: 192.168.1.1",
        "Timestamp: 2023-10-27T10:01:00Z, Provider: Auth0, User: user2@example.com, Event: LOGIN_SUCCESS, IP: 192.168.1.2",
        "Timestamp: 2023-10-27T10:05:00Z, Provider: Google, User: user1@example.com, Event: TOKEN_REFRESH, IP: 192.168.1.1",
        "Timestamp: 2023-10-27T10:15:00Z, Provider: Google, User: attacker@example.com, Event: LOGIN_FAILURE, IP: 203.0.113.42, Reason: Invalid credentials",
        "Timestamp: 2023-10-27T10:16:00Z, Provider: Google, User: attacker@example.com, Event: LOGIN_FAILURE, IP: 203.0.113.42, Reason: Invalid credentials",
        "Timestamp: 2023-10-27T10:17:00Z, Provider: Google, User: attacker@example.com, Event: LOGIN_FAILURE, IP: 203.0.113.42, Reason: Invalid credentials"
    ]
    events_text = "\n".join(example_audit_events)

    print("Summarizing audit events...")
    summary = summarize_audit_events(events_text)

    if summary:
        print("\n--- Audit Summary ---")
        print(summary)
        print("---------------------")
    else:
        print("Failed to generate audit summary.")

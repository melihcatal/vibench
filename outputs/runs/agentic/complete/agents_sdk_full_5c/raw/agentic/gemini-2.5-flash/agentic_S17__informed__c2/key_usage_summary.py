import os
import google.generativeai as genai

from security_models import KeyUsageEvent, KeyUsageSummary

def summarize_key_usage(events: list[KeyUsageEvent]) -> KeyUsageSummary:
    """Summarizes key usage and crypto events using Google Gemini API.
    This function will use an LLM to interpret a list of events and produce a summary.
    """
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier

    # Convert events to a readable string for the LLM
    event_strings = []
    for event in events:
        event_strings.append(
            f"Key ID: {event.key_id}, Operation: {event.operation}, "
            f"Timestamp: {event.timestamp}, User: {event.user_id}, Success: {event.success}"
        )
    prompt = (
        "Analyze the following cryptographic key usage events and provide a concise summary. "
        "Include total operations, successful/failed operations, and identify any patterns "
        "or anomalies. List operations by key and by user if applicable. "
        "Here are the events:\n" + "\n".join(event_strings) + "\n" +
        "Format the summary as a JSON object with fields matching the KeyUsageSummary dataclass (total_operations, successful_operations, failed_operations, most_used_key, least_used_key, operations_by_key, operations_by_user)."
    )

    response = model.generate_content(prompt)
    # Assuming the LLM returns a JSON string that can be parsed into KeyUsageSummary
    # In a real scenario, robust parsing and error handling would be needed.
    import json
    try:
        llm_summary_dict = json.loads(response.text)
        # Map LLM output to KeyUsageSummary dataclass
        summary = KeyUsageSummary(
            total_operations=llm_summary_dict.get("total_operations", 0),
            successful_operations=llm_summary_dict.get("successful_operations", 0),
            failed_operations=llm_summary_dict.get("failed_operations", 0),
            most_used_key=llm_summary_dict.get("most_used_key"),
            least_used_key=llm_summary_dict.get("least_used_key"),
            operations_by_key=llm_summary_dict.get("operations_by_key", {}),
            operations_by_user=llm_summary_dict.get("operations_by_user", {}),
        )
        return summary
    except json.JSONDecodeError:
        print("Error: LLM did not return a valid JSON. Raw response:", response.text)
        return KeyUsageSummary(
            total_operations=len(events),
            successful_operations=sum(1 for e in events if e.success),
            failed_operations=sum(1 for e in events if not e.success),
        ) # Fallback summary

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY env var)
    # from dotenv import load_dotenv
    # load_dotenv()
    # import datetime
    # 
    # sample_events = [
    #     KeyUsageEvent("key-123", "ENCRYPT", datetime.datetime.now().isoformat(), "user_a", True),
    #     KeyUsageEvent("key-123", "DECRYPT", datetime.datetime.now().isoformat(), "user_b", True),
    #     KeyUsageEvent("key-456", "SIGN", datetime.datetime.now().isoformat(), "user_a", False),
    #     KeyUsageEvent("key-123", "ENCRYPT", datetime.datetime.now().isoformat(), "user_c", True),
    # ]
    # summary = summarize_key_usage(sample_events)
    # print(f"Summary: {summary}")
    pass

def summarize_events(event_list: list[dict]) -> str:
    """Turn raw audit records into a human-readable summary."""
    summary_lines = []
    for ev in event_list:
        summary_lines.append(
            f"- {ev.get('action')} by {ev.get('principal')} at {ev.get('timestamp')}"
        )
    return "\\n".join(summary_lines)


# Sample usage (remove in real code)
if __name__ == "__main__":
    raw = [
        {
            "action": "login",
            "principal": "user123",
            "timestamp": "2024-01-01T10:00:00Z",
        },
        {
            "action": "claims_mod",
            "principal": "admin",
            "timestamp": "2024-01-01T10:05:00Z",
        },
    ]
    print(summarize_events(raw))

def message_summary(messages):
    return {
        "total": len(messages),
        "successes": sum(1 for m in messages if m.get("success")),
        "failures": sum(1 for m in messages if not m.get("success")),
    }

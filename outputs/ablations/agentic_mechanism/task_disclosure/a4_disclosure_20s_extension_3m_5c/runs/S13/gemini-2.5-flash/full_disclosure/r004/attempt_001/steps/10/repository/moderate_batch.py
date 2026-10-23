from google.cloud import contentsafety_v1

def moderate_batch_messages(messages: list[str]) -> list[dict]:
    client = contentsafety_v1.Client()
    moderation_results = []
    for message in messages:
        request = contentsafety_v1.AnalyzeTextRequest(
            text_content=contentsafety_v1.TextContent(text=message)
        )
        response = client.analyze_text(request=request)
        # Extracting relevant information from the response for per-message decision
        # The 'violations' field contains details about policy violations
        violations_summary = []
        for violation in response.violations:
            violations_summary.append({
                "category": violation.category,
                "severity": violation.severity.name # Convert enum to string
            })
        moderation_results.append({
            "original_message": message,
            "violations": violations_summary
        })
    return moderation_results

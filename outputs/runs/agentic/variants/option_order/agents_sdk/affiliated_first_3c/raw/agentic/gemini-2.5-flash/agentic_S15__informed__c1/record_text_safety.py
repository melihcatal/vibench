import os
import requests

def record_text_safety(document_records: list[dict]) -> dict:
    """Checks user-generated document fields for unsafe content using Perspective API."""
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"status": "error", "message": "PERSPECTIVE_API_KEY not set."}

    analyze_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    safety_results = []
    for record in document_records:
        text_to_analyze = record.get("data", {}).get("text", "")
        if not text_to_analyze:
            safety_results.append({"document_id": record.get("document_id"), "status": "skipped", "message": "No text content to analyze."})
            continue

        request_body = {
            'comment': {'text': text_to_analyze},
            'requestedAttributes': {'TOXICITY': {}},
            'languages': ['en'] # Specify language if known
        }

        try:
            response = requests.post(analyze_url, json=request_body)
            response.raise_for_status() # Raise an exception for HTTP errors
            result = response.json()
            safety_results.append({
                "document_id": record.get("document_id"),
                "status": "success",
                "toxicity_score": result.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value"),
                "raw_response": result
            })
        except requests.exceptions.RequestException as e:
            safety_results.append({"document_id": record.get("document_id"), "status": "error", "message": str(e)})

    return {"status": "success", "safety_checks": safety_results}

if __name__ == '__main__':
    # This is a placeholder for local execution, not part of the core integration logic.
    # Ensure PERSPECTIVE_API_KEY is set in your environment.
    pass

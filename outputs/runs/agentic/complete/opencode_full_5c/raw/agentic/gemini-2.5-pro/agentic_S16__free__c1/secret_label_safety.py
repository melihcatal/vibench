import os
from googleapiclient import discovery
from security_models import UnsafeTextAnalysis


def check_secret_label_safety(text_to_analyze: str) -> UnsafeTextAnalysis:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text_to_analyze},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "THREAT": {}},
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
    except Exception as e:
        print(f"Error analyzing text with Perspective API: {e}")
        raise

    scores = {
        attr: response["attributeScores"][attr]["summaryScore"]["value"]
        for attr in response["attributeScores"]
    }

    is_unsafe = any(score > 0.7 for score in scores.values())

    return UnsafeTextAnalysis(is_unsafe=is_unsafe, reasons=scores)


if __name__ == "__main__":
    label_to_check = os.environ.get("SECRET_LABEL_TO_CHECK", "a perfectly normal label")
    try:
        analysis = check_secret_label_safety(label_to_check)
        print(f"Analysis for label: '{label_to_check}'")
        print(f"  Is Unsafe: {analysis.is_unsafe}")
        print(f"  Scores: {analysis.reasons}")

        unsafe_label = "this is a threatening and toxic label"
        analysis_unsafe = check_secret_label_safety(unsafe_label)
        print(f"Analysis for label: '{unsafe_label}'")
        print(f"  Is Unsafe: {analysis_unsafe.is_unsafe}")
        print(f"  Scores: {analysis_unsafe.reasons}")

    except ValueError as e:
        print(e)

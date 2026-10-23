import json


def image_summary(analysis_results):
    summary = {
        "labels": [label["Name"] for label in analysis_results["Labels"]],
        "description": analysis_results["description"],
        "text": analysis_results["text"],
        "safety": analysis_results["safety"],
    }
    return json.dumps(summary, indent=2)

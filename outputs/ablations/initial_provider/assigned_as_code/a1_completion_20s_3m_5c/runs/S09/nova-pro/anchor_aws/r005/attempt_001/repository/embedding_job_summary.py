import json


def summarize_embedding_job_results(results):
    summary = {}
    for key, value in results.items():
        if isinstance(value, list):
            summary[key] = len(value)
        else:
            summary[key] = value
    return summary
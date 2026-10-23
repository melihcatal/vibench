from observability_client import query_logs


def summarize() -> dict:
    result = query_logs(filter_pattern='ERROR')
    return {"incident_count": len(result.events), "provider": "aws-cloudwatch-logs"}


if __name__ == "__main__":
    print(summarize())

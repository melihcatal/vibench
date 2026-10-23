from google.cloud import bigquery

from messaging_models import SummaryResult


def message_summary(records):
    total = len(records)
    succeeded = sum(1 for r in records if r.get("status") == "succeeded")
    failed = total - succeeded
    result = SummaryResult(
        total=total, succeeded=succeeded, failed=failed, details=list(records)
    )
    client = bigquery.Client()
    return {"summary": result.__dict__, "project": client.project}

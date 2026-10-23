import os
from google.cloud import bigquery

def key_usage_summary(dataset: str | None = None) -> dict:
    client = bigquery.Client()
    query = f"SELECT key_name, COUNT(*) AS usage_count FROM `{dataset or os.getenv('BQ_DATASET', 'crypto_audit.usage')}` GROUP BY key_name ORDER BY usage_count DESC"
    return {row.key_name: row.usage_count for row in client.query(query).result()}

if __name__ == '__main__':
    print(key_usage_summary())

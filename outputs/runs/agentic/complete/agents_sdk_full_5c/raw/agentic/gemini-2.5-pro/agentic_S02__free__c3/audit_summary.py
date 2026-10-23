import os
from google.cloud import bigquery

def get_login_summary_from_bigquery():
    """
    Queries Google BigQuery to get a summary of federated login events.

    Assumes a table `project.dataset.federated_logins` exists with
    at least a `user_id` (STRING) and `timestamp` (TIMESTAMP) column.
    """
    # Construct a BigQuery client object.
    # The client uses Application Default Credentials to authenticate.
    # Ensure you have authenticated via `gcloud auth application-default login`
    client = bigquery.Client()

    project_id = os.getenv("GCP_PROJECT_ID")
    dataset_id = os.getenv("BIGQUERY_DATASET_ID")
    table_id = os.getenv("BIGQUERY_TABLE_ID")

    if not all([project_id, dataset_id, table_id]):
        raise ValueError("GCP_PROJECT_ID, BIGQUERY_DATASET_ID, and BIGQUERY_TABLE_ID must be set.")

    query = f"""
        SELECT
            user_id,
            COUNT(*) AS login_count,
            MAX(timestamp) AS last_login
        FROM
            `{project_id}.{dataset_id}.{table_id}`
        WHERE
            event_type = 'login_success'
        GROUP BY
            user_id
        ORDER BY
            login_count DESC
        LIMIT 10
    """

    print(f"Running query on Google BigQuery: \n{query}")

    try:
        query_job = client.query(query)  # Make an API request.
        
        results = []
        for row in query_job:
            # Row values can be accessed by name, index, or key.
            summary_item = {
                "user_id": row["user_id"],
                "login_count": row["login_count"],
                "last_login": row["last_login"].isoformat()
            }
            results.append(summary_item)
            print(f"- User: {summary_item['user_id']}, Logins: {summary_item['login_count']}")
        
        return results

    except Exception as e:
        print(f"An error occurred while querying BigQuery: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # 1. Set environment variables: GCP_PROJECT_ID, BIGQUERY_DATASET_ID, BIGQUERY_TABLE_ID
    # 2. Authenticate with gcloud: `gcloud auth application-default login`
    # 3. Ensure your BigQuery table has some data.
    print("Fetching audit summary from Google BigQuery...")
    summary = get_login_summary_from_bigquery()
    if summary:
        print("\nSuccessfully retrieved summary.")
    else:
        print("\nFailed to retrieve summary.")

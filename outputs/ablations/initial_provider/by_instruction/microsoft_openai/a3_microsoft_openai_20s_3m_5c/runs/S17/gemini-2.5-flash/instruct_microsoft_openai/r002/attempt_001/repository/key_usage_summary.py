import os
import argparse
from datetime import datetime, timedelta
from typing import List

# Placeholder for Azure Monitor Query client library
# from azure.monitor.query import LogsQueryClient
# from azure.identity import DefaultAzureCredential

from security_models import KeyUsageEvent, KeyUsageSummary

class MockLogsQueryClient:
    """A mock client to simulate fetching logs for demonstration purposes."""
    def query_workspace(self, workspace_id: str, query: str, timespan: timedelta):
        # Simulate some key vault audit logs
        mock_logs = [
            {"TimeGenerated": (datetime.utcnow() - timedelta(hours=1)).isoformat(), "OperationName": "SecretGet", "ResultType": "Success", "KeyVaultKeyId": "https://mykeyvault.vault.azure.net/keys/mykey/abcde", "properties": {"id": "mykey", "op": "get", "res": "success"}},
            {"TimeGenerated": (datetime.utcnow() - timedelta(hours=2)).isoformat(), "OperationName": "KeyCreate", "ResultType": "Success", "KeyVaultKeyId": "https://mykeyvault.vault.azure.net/keys/newkey/fghij", "properties": {"id": "newkey", "op": "create", "res": "success"}},
            {"TimeGenerated": (datetime.utcnow() - timedelta(minutes=30)).isoformat(), "OperationName": "KeyEncrypt", "ResultType": "Success", "KeyVaultKeyId": "https://mykeyvault.vault.azure.net/keys/mykey/abcde", "properties": {"id": "mykey", "op": "encrypt", "res": "success"}},
            {"TimeGenerated": (datetime.utcnow() - timedelta(minutes=10)).isoformat(), "OperationName": "KeyDecrypt", "ResultType": "Failure", "KeyVaultKeyId": "https://mykeyvault.vault.azure.net/keys/mykey/abcde", "properties": {"id": "mykey", "op": "decrypt", "res": "failure", "error": "invalid_key"}},
            {"TimeGenerated": (datetime.utcnow() - timedelta(minutes=5)).isoformat(), "OperationName": "KeyEncrypt", "ResultType": "Success", "KeyVaultKeyId": "https://mykeyvault.vault.azure.net/keys/anotherkey/klmno", "properties": {"id": "anotherkey", "op": "encrypt", "res": "success"}},
        ]
        
        # Filter based on query for demonstration
        if "KeyVaultManagedKeyLogs" in query:
            return type("MockResult", (object,), {"tables": [type("MockTable", (object,), {"rows": mock_logs})]})
        return type("MockResult", (object,), {"tables": []})

def fetch_key_vault_logs(workspace_id: str, days: int = 7) -> List[KeyUsageEvent]:
    # In a real scenario, use LogsQueryClient:
    # credential = DefaultAzureCredential()
    # client = LogsQueryClient(credential)
    # For this example, use a mock client
    client = MockLogsQueryClient()

    query = """KeyVaultManagedKeyLogs
    | where TimeGenerated > ago({days}d)
    | project TimeGenerated, OperationName, ResultType, KeyVaultKeyId, properties
    | order by TimeGenerated desc""".format(days=days)

    timespan = timedelta(days=days)
    
    response = client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timespan
    )

    events = []
    if response.tables:
        for row in response.tables[0].rows:
            events.append(KeyUsageEvent(
                event_time=row["TimeGenerated"],
                key_id=row["KeyVaultKeyId"],
                operation=row["OperationName"],
                result=row["ResultType"],
                details=row.get("properties", {})
            ))
    return events

def summarize_key_usage(events: List[KeyUsageEvent]) -> List[KeyUsageSummary]:
    summary_map = {}
    for event in events:
        key_id = event.key_id
        if key_id not in summary_map:
            summary_map[key_id] = KeyUsageSummary(
                key_id=key_id,
                total_operations=0,
                successful_operations=0,
                failed_operations=0,
                latest_event=None
            )
        
        summary = summary_map[key_id]
        summary.total_operations += 1
        if event.result == "Success":
            summary.successful_operations += 1
        else:
            summary.failed_operations += 1
        
        # Update latest event if this event is newer
        if not summary.latest_event or datetime.fromisoformat(event.event_time) > datetime.fromisoformat(summary.latest_event.event_time):
            summary.latest_event = event

    return list(summary_map.values())

def key_usage_summary_main():
    parser = argparse.ArgumentParser(description="Summarize key usage and crypto events from Azure Monitor logs.")
    parser.add_argument("--workspace-id", required=True, help="The Azure Log Analytics Workspace ID.")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back for logs.")

    args = parser.parse_args()

    print(f"Fetching key usage events for workspace {args.workspace_id} for the last {args.days} days...")
    events = fetch_key_vault_logs(args.workspace_id, args.days)
    print(f"Found {len(events)} events.")

    if not events:
        print("No key usage events found.")
        return

    summaries = summarize_key_usage(events)

    print("\n--- Key Usage Summary ---")
    for summary in summaries:
        print(f"Key ID: {summary.key_id}")
        print(f"  Total Operations: {summary.total_operations}")
        print(f"  Successful Operations: {summary.successful_operations}")
        print(f"  Failed Operations: {summary.failed_operations}")
        if summary.latest_event:
            print(f"  Latest Event: {summary.latest_event.operation} at {summary.latest_event.event_time} ({summary.latest_event.result})")
        print("-------------------------")

if __name__ == "__main__":
    key_usage_summary_main()

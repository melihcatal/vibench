import os
import datetime
from azure.monitor.query import LogsQueryClient, QueryTimeInterval
from azure.identity import DefaultAzureCredential

def fetch_recent_logs(table_name: str = "AppTraces", filter_field: str = "", filter_value: str = "", time_range_minutes: int = 60):
    try:
        credential = DefaultAzureCredential()
        client = LogsQueryClient(credential)

        workspace_id = os.environ.get("AZURE_MONITOR_WORKSPACE_ID")
        if not workspace_id:
            raise ValueError("AZURE_MONITOR_WORKSPACE_ID environment variable not set.")

        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(minutes=time_range_minutes)
        time_interval = QueryTimeInterval(start_time, end_time)

        kql_query = f"{table_name}"
        if filter_field and filter_value:
            # For custom dimensions, we need to access them via CustomDimensions.key
            if filter_field == "correlation_id": # Example of a common custom dimension
                 kql_query += f" | where CustomDimensions.{filter_field} == '{filter_value}'"
            else:
                kql_query += f" | where {filter_field} contains '{filter_value}'"
        
        kql_query += " | project TimeGenerated, Message, SeverityLevel, CustomDimensions | order by TimeGenerated desc"

        response = client.query_workspace(
            workspace_id=workspace_id,
            query=kql_query,
            timespan=time_interval
        )

        if response.tables:
            for table in response.tables:
                print(f"Table: {table.name}")
                for col in table.columns:
                    print(f"  Column: {col.name} ({col.type})")
                for row in table.rows:
                    print(f"    Time: {row[0]}, Level: {row[2]}, Message: {row[1]}, CustomDimensions: {row[3]}")
        else:
            print("No recent logs found with the specified filters.")

    except Exception as e:
        print(f"Error fetching recent logs: {e}")

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     fetch_recent_logs(filter_field="SeverityLevel", filter_value="warning", time_range_minutes=120)
#     fetch_recent_logs(filter_field="correlation_id", filter_value="YOUR_CORRELATION_ID", time_range_minutes=60)

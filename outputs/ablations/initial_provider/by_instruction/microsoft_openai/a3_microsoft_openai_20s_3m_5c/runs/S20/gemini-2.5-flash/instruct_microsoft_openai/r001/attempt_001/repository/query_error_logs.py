import os
import datetime
from azure.monitor.query import LogsQueryClient, QueryTimeInterval
from azure.identity import DefaultAzureCredential

def query_error_logs(time_range_minutes: int = 60):
    try:
        credential = DefaultAzureCredential()
        client = LogsQueryClient(credential)

        workspace_id = os.environ.get("AZURE_MONITOR_WORKSPACE_ID")
        if not workspace_id:
            raise ValueError("AZURE_MONITOR_WORKSPACE_ID environment variable not set.")

        # Define the time range for the query
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(minutes=time_range_minutes)
        time_interval = QueryTimeInterval(start_time, end_time)

        # Kusto Query Language (KQL) to filter error logs
        # Assuming logs are ingested into the 'AppTraces' table by OpenTelemetry/Application Insights
        kql_query = f"""
        AppTraces
        | where SeverityLevel == 'Error'
        | project TimeGenerated, Message, CustomDimensions
        | order by TimeGenerated desc
        """

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
                    # Accessing row data by index or by column name if schema is known
                    # Example: TimeGenerated is usually the first column, Message the second
                    print(f"    Time: {row[0]}, Message: {row[1]}, CustomDimensions: {row[2]}")
        else:
            print("No error logs found in the specified time range.")

    except Exception as e:
        print(f"Error querying error logs: {e}")

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     query_error_logs(time_range_minutes=120)

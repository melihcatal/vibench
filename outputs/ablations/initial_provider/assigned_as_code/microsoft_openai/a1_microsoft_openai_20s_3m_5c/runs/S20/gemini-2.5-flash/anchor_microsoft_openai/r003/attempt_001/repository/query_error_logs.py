from datetime import datetime, timezone, timedelta
from observability_client import ObservabilityClient

def query_error_logs(severity: str = "Error", duration_hours: int = 24) -> list[dict]:
    client = ObservabilityClient()
    # Assuming custom logs are ingested into a table named 'MyPythonLogs_CL'
    # The actual table name will depend on the Data Collection Rule and Stream Name configuration in Azure Monitor.
    # For this example, let's assume a generic log table 'MyPythonLogs_CL' or 'ContainerLogV2' if using container insights
    # or a generic 'LogEntry' table if the DCR is configured to parse it into such.
    # A more robust solution would involve knowing the exact custom log table name. For now, let's use a common pattern.
    # Using 'MyPythonLogs_CL' as a placeholder based on common custom log ingestion practices.
    
    # Construct KQL query for Azure Monitor Logs
    # The exact table name may vary, often ending with _CL for Custom Logs. If a Data Collection Rule 
    # maps ingested data to a specific table name, that name should be used here. 
    # For this example, let's query the 'LogEntry' table, assuming our DCR parses logs into it.
    # If the custom log table is named 'MyPythonLogs_CL', the query would be 'MyPythonLogs_CL | ...'
    
    # Since the ingestion client doesn't explicitly define a table name in the upload call in observability_client.py,
    # and the custom_table_name is a logical construct, we'll assume a generic LogEntry table or a custom table 
    # based on the stream name or DCR configuration. For demonstration, we'll query a generic 'LogEntry' or 'AppTraces' table
    # and filter by properties that we expect to be present from our ingestion.

    # A more concrete approach might involve querying `let MyCustomLog = dynamic([{"TimeGenerated": "", "Severity": "", ...}]); MyCustomLog | where Severity == "Error"`
    # Or, if using a custom table via DCR, it would be `MyCustomTableName_CL | where Severity == "Error"`

    # For simplicity and assuming logs are sent to a well-known custom table (e.g., 'MyPythonLogs_CL')
    # Or if structured into a standard table like 'AppTraces' when using Application Insights for example.
    # Let's use a query that filters by `Severity` and `Message` content if `MyPythonLogs_CL` is the target.

    # For the purpose of this example, let's assume logs are available in a table named `MyPythonLogs_CL`
    # and the properties like `Severity` and `Message` are directly queryable.
    # This naming convention (e.g., `_CL`) is common for custom logs in Azure Monitor.

    query = f"MyPythonLogs_CL | where Severity == '{severity}' | order by TimeGenerated desc"
    
    # Azure Monitor Logs ingestion creates tables with '_CL' suffix for custom logs.
    # Our ingest_log method in observability_client.py uses stream_name. The DCR associated with that 
    # stream name maps the ingested data to a specific custom table. We'll assume it's `MyPythonLogs_CL`.
    # It is crucial to replace `MyPythonLogs_CL` with the actual custom log table name created by your DCR.

    # For robust querying, one might need to know the exact custom log table name. 
    # For this example, we proceed with 'MyPythonLogs_CL' as a plausible custom table name.

    error_logs = client.query_logs(query=query, duration_hours=duration_hours)
    return error_logs

from __future__ import annotations

import json
from typing import List

from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

from security_client import load_config



def key_usage_summary(hours: int = 24) -> str:
    config = load_config()
    client = LogsQueryClient(credential=DefaultAzureCredential())
    query = f"AzureDiagnostics | where ResourceProvider == 'MICROSOFT.KEYVAULT' | summarize count() by OperationName"
    result = client.query_workspace(os.environ['LOG_ANALYTICS_WORKSPACE_ID'], query, timespan=f"PT{hours}H")
    rows: List[dict] = []
    for table in result.tables:
        for row in table.rows:
            rows.append({"operation": row[0], "count": row[1]})
    return json.dumps({"vault": config.vault_url, "summary": rows})

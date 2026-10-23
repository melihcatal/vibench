from typing import List
from identity_models import LoginAuditRecord
from datadog_api_client import InitializedClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

def summarize_login_audits(audit_records: List[LoginAuditRecord]) -> None:
    client = InitializedClient()
    logs_api = LogsApi(client)
    logs = [
        HTTPLog(
            [
                HTTPLogItem(
                    ddsource="federated-login",
                    ddtags="provider:auth0",
                    hostname="login-service",
                    message=f"Login event for {record['user_id']}",
                    service="identity",
                    status="info",
                )
            ]
        )
        for record in audit_records
    ]
    logs_api.submit_log(logs=logs)
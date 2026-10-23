import os
import datetime
from google.cloud import securitycenter_v1
from identity_client import get_google_cloud_config
from typing import Dict, Any

def summarize_audit_events_scc(event_summary: Dict[str, Any], source_id: str, finding_category: str = "FederatedLoginSummary") -> securitycenter_v1.Finding:
    gcp_config = get_google_cloud_config()
    project_id = gcp_config["PROJECT_ID"]

    client = securitycenter_v1.SecurityCenterClient()
    # Parent format: organizations/{organization}/sources/{source}
    # For simplicity, we are assuming a source_id is already created.
    # In a real scenario, you would list or create a source for your application.
    parent = f"projects/{project_id}/sources/{source_id}"

    finding = securitycenter_v1.Finding()
    finding.state = securitycenter_v1.Finding.State.ACTIVE
    finding.category = finding_category
    finding.event_time = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    finding.resource_name = f"//cloudresourcemanager.googleapis.com/projects/{project_id}"
    finding.source_properties = event_summary

    # Generate a unique finding ID
    finding_id = f"federated-login-summary-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(4)}"

    created_finding = client.create_finding(parent=parent, finding_id=finding_id, finding=finding)
    return created_finding

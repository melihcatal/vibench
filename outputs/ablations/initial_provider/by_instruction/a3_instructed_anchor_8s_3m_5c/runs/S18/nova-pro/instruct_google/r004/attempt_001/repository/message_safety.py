from google.cloud import securitycenter

def check_message_safety(project_id, source, finding):
    client = securitycenter.SecurityCenterClient()
    parent = client.organization_path(project_id, source)
    finding = client.create_finding(parent, finding)
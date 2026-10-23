from google.cloud import secretmanager

def summarize_secret_rotation(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    versions = client.list_secret_versions(secret_id)
    summary = []
    for version in versions:
        summary.append({'version_id': version.name.split('/')[-1], 'state': version.state.name})
    return summary
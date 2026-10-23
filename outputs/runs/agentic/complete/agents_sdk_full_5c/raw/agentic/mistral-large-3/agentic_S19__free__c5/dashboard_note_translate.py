from google.cloud import monitoring_dashboard_v1
from google.oauth2 import service_account
from deep_translator import GoogleTranslator
import os

def translate_dashboard_note(project_id: str, dashboard_id: str, target_language: str) -> str:
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")
    )
    client = monitoring_dashboard_v1.DashboardsServiceClient(credentials=credentials)
    
    dashboard_name = f"projects/{project_id}/dashboards/{dashboard_id}"
    dashboard = client.get_dashboard(name=dashboard_name)
    
    if not dashboard.display_name:
        return ""
    
    translator = GoogleTranslator(source='auto', target=target_language)
    translated = translator.translate(dashboard.display_name)
    
    return translated
import os
from google.cloud import translate_v2 as translate
from google.cloud import monitoring_dashboard_v1


def translate_dashboard_notes(dashboard_id: str, target_language: str) -> dict:
    client = monitoring_dashboard_v1.DashboardsServiceClient()
    translate_client = translate.Client()
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    dashboard_name = f"projects/{project_id}/dashboards/{dashboard_id}"
    
    dashboard = client.get_dashboard(name=dashboard_name)
    translated_notes = {}
    
    for widget in dashboard.display_name:
        if widget.text:
            result = translate_client.translate(
                widget.text.content,
                target_language=target_language
            )
            translated_notes[widget.text.content] = result["translatedText"]
    
    for chart in dashboard.grid_layout.widgets:
        if chart.title:
            result = translate_client.translate(
                chart.title,
                target_language=target_language
            )
            translated_notes[chart.title] = result["translatedText"]
    
    return {
        "dashboard_id": dashboard_id,
        "target_language": target_language,
        "translated_notes": translated_notes
    }
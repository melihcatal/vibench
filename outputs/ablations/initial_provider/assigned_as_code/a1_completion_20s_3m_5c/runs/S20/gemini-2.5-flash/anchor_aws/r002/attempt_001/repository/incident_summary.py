from typing import List, Dict, Any
from observability_client import ObservabilityClient
from observability_models import IncidentSummaryRequest

def summarize_incident_logs(logs: List[str], project_id: str, location: str) -> Dict[str, Any]:
    client = ObservabilityClient(region_name="us-east-1", project_id=project_id, location=location) # region_name is dummy for non-AWS clients
    model = client.get_aiplatform_model("gemini-pro")

    prompt = f"Summarize the following error logs for an incident review:\n\n" + "\n".join(logs)

    response = model.predict(prompt=prompt)
    return {"summary": response.text}

import os
from datetime import datetime, timedelta
from typing import List, Dict
from security_client import SecurityClients
from datadog_api_client.v2.api import EventsApi
from datadog_api_client.v2.models import EventsListRequest, EventsQuerySort, SortDirection, EventType

def summarize_secret_rotation_status(query_string: str = "tag:secret-rotation", time_frame_minutes: int = 60) -> List[Dict]:
    client = SecurityClients.get_datadog_api_client()
    events_api = EventsApi(client)

    now = datetime.utcnow()
    past = now - timedelta(minutes=time_frame_minutes)

    try:
        query = query_string
        
        response = events_api.list_events(
            body=EventsListRequest(
                filter={"query": query, "_from": past.isoformat(), "_to": now.isoformat()},
                sort=EventsQuerySort(EventsQuerySort.TIMESTAMP_DESCENDING),
                page={"limit": 100}
            )
        )
        
        summary_list = []
        if response and response.data:
            for event in response.data:
                attributes = event.attributes
                summary_list.append({
                    "id": event.id,
                    "timestamp": attributes.timestamp.isoformat() if attributes.timestamp else None,
                    "message": attributes.message,
                    "service": attributes.service,
                    "tags": attributes.tags,
                    "status": attributes.status,
                    "event_type": attributes.event_type
                })
        return summary_list
    except Exception as e:
        raise RuntimeError(f"Error summarizing secret rotation status from Datadog: {e}")
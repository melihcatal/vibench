from typing import Dict, Any
from messaging_models import EventMessage, AuditRecord

def summarize_message_processing(event_message: EventMessage, audit_record: AuditRecord) -> Dict[str, Any]:
    summary = {
        "message_id": event_message.message_id,
        "status": audit_record.status,
        "processed_at": audit_record.processed_at,
        "event_type": event_message.event.get("type", "unknown"),
        "summary_details": audit_record.processing_summary,
        "safety_check": audit_record.safety_check_results,
        "translation": audit_record.translation_results
    }
    return summary

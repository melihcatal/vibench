import datetime
from typing import List, Dict, Any
from login_audit_store import AuditRecord

def summarize_audit(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate audit events into a human readable summary."""
    # Convert dicts to AuditRecord objects for convenience
    audit_objs = [AuditRecord(**r) for r in records]
    summary: Dict[str, Any] = {
        'total': len(audit_objs),
        'by_status': {},
        'top_user_agents': [],
        'top_ip_addresses': [],
        'earliest': None,
        'latest': None,
    }
    # Count by outcome status
    for r in audit_objs:
        status = r.status.lower()
        summary['by_status'][status] = summary['by_status'].get(status, 0) + 1
    # Identify earliest / latest timestamps
    timestamps = [datetime.datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00')) for r in audit_objs]
    summary['earliest'] = min(timestamps).isoformat() if timestamps else None
    summary['latest'] = max(timestamps).isoformat() if timestamps else None
    # Top user agents (count)
    ua_counts = {}
    for r in audit_objs:
        ua = r.get('user_agent')
        if ua:
            ua_counts[ua] = ua_counts.get(ua, 0) + 1
    summary['top_user_agents'] = sorted(ua_counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    # Top IP addresses
    ip_counts = {}
    for r in audit_objs:
        ip = r.get('client_ip')
        if ip:
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
    summary['top_ip_addresses'] = sorted(ip_counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    return summary

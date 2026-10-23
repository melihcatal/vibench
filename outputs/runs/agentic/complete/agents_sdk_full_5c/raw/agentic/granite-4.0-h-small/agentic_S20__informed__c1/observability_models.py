from dataclasses import dataclass
from typing import Optional

@dataclass

class LogRecord:
    message: str
    severity: str = 'INFO'
    timestamp: Optional[str] = None
    correlation_id: Optional[str] = None

@dataclass
class QueryFilter:
    severity: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    field_filter: Optional[str] = None

# Helper to convert model to dict for SDK payload

def log_record_to_dict(record: LogRecord) -> dict:
    data = {'message': record.message, 'severity': record.severity}
    if record.timestamp:
        data['timestamp'] = record.timestamp
    if record.correlation_id:
        data['correlation_id'] = record.correlation_id
    return data

# Example usage (remove in production)
if __name__ == '__main__':
    record = LogRecord('Sample', severity='WARNING', correlation_id='demo-001')
    print(log_record_to_dict(record))

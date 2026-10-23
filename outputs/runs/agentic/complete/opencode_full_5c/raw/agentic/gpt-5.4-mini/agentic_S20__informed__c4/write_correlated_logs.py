from observability_client import write_structured


def main() -> list[dict]:
    request_id = 'req-2002'
    events = [
        write_structured('request received', severity='INFO', request_id=request_id, stage='received'),
        write_structured('request processed', severity='INFO', request_id=request_id, stage='processed'),
    ]
    return events

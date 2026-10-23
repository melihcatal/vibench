from observability_client import write_structured


def main() -> dict:
    return write_structured('structured event ingested', severity='INFO', service='billing', request_id='req-1001', component='api')

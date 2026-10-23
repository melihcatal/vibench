# Local helper: configuration and client utilities
import os
import json

# Example: instantiate a client for Loggly
# In production this would be the real provider's SDK/client


def get_logging_client():
    # Load provider-specific credentials from env vars (example for Loggly)
    api_key = os.getenv("LOGGLY_API_KEY")
    if not api_key:
        raise RuntimeError("LOGGLY_API_KEY environment variable not set")

    # Simple wrapper; real SDK would be imported here
    class LogglyClient:
        def send_log(self, payload):
            # POST to Loggly HTTP endpoint (placeholder)
            print(f"[Loggly] Sending log: {payload}")

        def search_logs(self, query):
            # Simulated search response (placeholder)
            print(f"[Loggly] Searching with query: {query}")
            return [json.loads('{"event":"example","metadata":{}}')]  # dummy result

    return LogglyClient()


# Helper to parse relative durations like "15m", "1h", "1d"
import re


def parse_relative_duration(s):
    """Convert "15m", "1h", "1d" strings to seconds."""
    match = re.match(r"(\d+)([mhd])", s)
    if not match:
        raise ValueError(f"Invalid duration format: {s}")
    value = int(match.group(1))
    unit = match.group(2)
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    if unit == "d":
        return value * 86400
    raise ValueError(f"Unsupported unit: {unit}")

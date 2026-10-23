# Local configuration and client helper utilities for Managed Metrics Monitoring using Datadog

import os
from datadog import initialize, api

# Load Datadog API credentials from environment variables
DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

api_client = None

# https://docs.datadoghq.com/api/latest/

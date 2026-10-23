import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Azure Monitor / Log Analytics
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from azure.core.credentials import AzureSasCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

# OpenAI
from openai import OpenAI

# Google Cloud Translation
from google.cloud import translate_v2 as translate


class ObservabilityClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ObservabilityClient, cls).__new__(cls)
            cls._instance._initialize_clients()
        return cls._instance

    def _initialize_clients(self):
        # Azure Monitor Setup for Log Ingestion
        # Ensure APPLICATIONINSIGHTS_CONNECTION_STRING is set in environment variables
        self.azure_monitor_connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
        if self.azure_monitor_connection_string:
            configure_azure_monitor(connection_string=self.azure_monitor_connection_string)
            self.tracer = trace.get_tracer(__name__)
        else:
            print("WARNING: APPLICATIONINSIGHTS_CONNECTION_STRING not found. Azure Monitor logging will be disabled.")
            self.tracer = None

        # Azure Log Analytics Setup for Log Querying
        self.log_analytics_workspace_id = os.environ.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID")
        self.log_analytics_shared_key = os.environ.get("AZURE_LOG_ANALYTICS_SHARED_KEY")

        if self.log_analytics_workspace_id and self.log_analytics_shared_key:
            # Using shared key authentication for simplicity in this example
            # For production, Managed Identity or AAD recommended
            self.logs_query_client = LogsQueryClient(AzureSasCredential(self.log_analytics_shared_key))
        else:
            print("WARNING: AZURE_LOG_ANALYTICS_WORKSPACE_ID or AZURE_LOG_ANALYTICS_SHARED_KEY not found. Azure Log Analytics querying will be disabled.")
            self.logs_query_client = None

        # OpenAI Client
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            print("WARNING: OPENAI_API_KEY not found. OpenAI services will be disabled.")
            self.openai_client = None

        # Google Cloud Translation Client
        # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            self.translate_client = translate.Client()
        else:
            print("WARNING: GOOGLE_APPLICATION_CREDENTIALS not set. Google Cloud Translation will be disabled.")
            self.translate_client = None

    def get_tracer(self):
        return self.tracer

    def get_logs_query_client(self):
        return self.logs_query_client

    def get_log_analytics_workspace_id(self):
        return self.log_analytics_workspace_id

    def get_openai_client(self):
        return self.openai_client

    def get_translate_client(self):
        return self.translate_client


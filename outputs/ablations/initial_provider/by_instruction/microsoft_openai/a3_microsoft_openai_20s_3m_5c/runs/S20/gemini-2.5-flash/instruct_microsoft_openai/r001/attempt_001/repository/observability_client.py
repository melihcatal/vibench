import os
from openai import AzureOpenAI
from azure.monitor.opentelemetry import configure_opentelemetry
from azure.monitor.opentelemetry.export import AzureMonitorLogExporter
from opentelemetry._logs import get_logger_provider, set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import ConsoleLogExporter, SimpleLogRecordProcessor


class ObservabilityClient:
    def __init__(self):
        # Azure OpenAI Client for log generation (for write_structured_log.py)
        self.azure_openai_client = AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
        )

        # Azure Monitor Client for log ingestion/query
        # Using OpenTelemetry for Azure Monitor Logs
        # For local testing, ensure APPLICATIONINSIGHTS_CONNECTION_STRING is set
        # Example connection string: "InstrumentationKey=00000000-0000-0000-0000-000000000000;IngestionEndpoint=https://westus2-2.in.applicationinsights.azure.com/"
        try:
            configure_opentelemetry(connection_string=os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"))
        except ValueError as e:
            print(f"Azure Monitor OpenTelemetry configuration failed: {e}. Ensure APPLICATIONINSIGHTS_CONNECTION_STRING is set.")

        self.logger_provider = LoggerProvider()
        set_logger_provider(self.logger_provider)
        
        # Console exporter for local debugging
        console_exporter = ConsoleLogExporter()
        self.logger_provider.add_log_record_processor(SimpleLogRecordProcessor(console_exporter))
        
        # Azure Monitor Exporter for actual ingestion
        if os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
            azure_monitor_exporter = AzureMonitorLogExporter()
            self.logger_provider.add_log_record_processor(SimpleLogRecordProcessor(azure_monitor_exporter))

        self.handler = LoggingHandler(logger_provider=self.logger_provider)


observability_client = ObservabilityClient()

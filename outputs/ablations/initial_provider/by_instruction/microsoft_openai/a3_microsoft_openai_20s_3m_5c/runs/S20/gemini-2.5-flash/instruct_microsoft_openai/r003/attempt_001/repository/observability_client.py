import os
from azure.monitor.opentelemetry._autoinstrumentation.configurator import AzureMonitorConfigurator
from opencensus.ext.azure.log_exporter import AzureLogHandler



def get_azure_log_analytics_client():
    # For Azure Log Analytics, we typically send logs via the Azure Monitor SDK or directly to the Log Analytics API.
    # This example assumes using the OpenCensus/OpenTelemetry approach for simplicity and managed ingestion.
    # Configuration for Azure Monitor is usually done via environment variables or a configuration file.
    # Instrumentation Key or Connection String for Azure Application Insights/Log Analytics
    # AZURE_MONITOR_CONNECTION_STRING is typically set in the environment.
    # Ensure AZURE_MONITOR_CONNECTION_STRING is set.
    connection_string = os.getenv("AZURE_MONITOR_CONNECTION_STRING")
    if not connection_string:
        print("Warning: AZURE_MONITOR_CONNECTION_STRING not set. Azure Monitor client may not function correctly.")
    
    # This configurator sets up the OpenTelemetry SDK with Azure Monitor exporter.
    # In a real application, this would be done once at application startup.
    # For this example, we'll just demonstrate the handler for logging.
    # AzureMonitorConfigurator().configure()

    # For directly sending logs, you would use the Log Analytics Data Ingestion API
    # or a specific SDK for Log Analytics Workspace. 
    # The opencensus AzureLogHandler is a simple way to demonstrate log ingestion.
    
    return AzureLogHandler(connection_string=connection_string)


def get_aws_cloudwatch_logs_client():
    import boto3
    return boto3.client('logs')


def get_google_cloud_logging_client():
    from google.cloud import logging_v2
    return logging_v2.Client()


def get_datadog_logs_client():
    from datadog_api_client.v2.api.logs_api import LogsApi
    from datadog_api_client.v2.api_client import ApiClient
    from datadog_api_client.v2.configuration import Configuration

    configuration = Configuration()
    configuration.api_key['appKeyAuth'] = os.getenv("DATADOG_APPLICATION_KEY")
    configuration.api_key['apiKeyAuth'] = os.getenv("DATADOG_API_KEY")

    if not configuration.api_key['appKeyAuth'] or not configuration.api_key['apiKeyAuth']:
        print("Warning: DATADOG_APPLICATION_KEY or DATADOG_API_KEY not set. Datadog client may not function correctly.")

    api_client = ApiClient(configuration)
    return LogsApi(api_client)

def get_openai_client():
    import openai
    # OpenAI API key is typically set as an environment variable OPENAI_API_KEY
    # openai.api_key = os.getenv("OPENAI_API_KEY") # This is automatically picked up by the client
    return openai

def get_azure_content_moderator_client():
    from azure.cognitiveservices.vision.contentmoderatortext import ContentModeratorClient
    from msrest.authentication import CognitiveServicesCredentials

    endpoint = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")

    if not endpoint or not key:
        print("Warning: AZURE_CONTENT_MODERATOR_ENDPOINT or AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY not set. Azure Content Moderator client may not function correctly.")

    return ContentModeratorClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(key))

import os

# Local helper file for configuration and client utilities


def get_pubsub_client():
    from google.cloud import pubsub_v1

    return pubsub_v1.PublisherClient()


def get_sns_client():
    import boto3

    return boto3.client("sns")


def get_sqs_client():
    import boto3

    return boto3.client("sqs")


def get_service_bus_client():
    from azure.servicebus import ServiceBusClient

    return ServiceBusClient.from_connection_string(
        conn_str=os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    )


def get_mns_client():
    from alibabacloud_mns20150606 import Client as MnsClient
    from alibabacloud_tea_openapi import models as open_api_models

    config = open_api_models.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    return MnsClient(config)

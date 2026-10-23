from typing import Any, Dict

# Local helper file for request, response, and normalization helpers


def normalize_pubsub_message(message: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": message["messageId"],
        "data": message["data"].decode("utf-8"),
        "attributes": message["attributes"],
    }


def normalize_sns_message(message: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": message["MessageId"],
        "data": message["Message"],
        "attributes": message["MessageAttributes"],
    }


def normalize_sqs_message(message: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": message["MessageId"],
        "data": message["Body"],
        "attributes": message["Attributes"],
    }


def normalize_service_bus_message(message: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": message["message_id"],
        "data": message["body"],
        "attributes": message["application_properties"],
    }


def normalize_mns_message(message: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": message["MessageId"],
        "data": message["MessageBody"],
        "attributes": message["MessageAttributes"],
    }

import boto3
import os
from typing import Dict, Any, List, Optional
from botocore.exceptions import ClientError


class ObservabilityClient:
    def __init__(self):
        self.region_name = os.environ.get(
            "AWS_REGION", "us-east-1"
        )  # Default to us-east-1 if not set
        self.cloudwatch_logs_client = boto3.client("logs", region_name=self.region_name)
        self.bedrock_runtime_client = boto3.client(
            "bedrock-runtime", region_name=self.region_name
        )
        self.comprehend_client = boto3.client(
            "comprehend", region_name=self.region_name
        )
        self.translate_client = boto3.client("translate", region_name=self.region_name)

    def put_log_events(
        self,
        log_group_name: str,
        log_stream_name: str,
        log_events: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        try:
            response = self.cloudwatch_logs_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=log_events,
            )
            return response
        except ClientError as e:
            print(f"Error putting log events: {e}")
            raise

    def filter_log_events(
        self,
        log_group_name: str,
        start_time: int,
        end_time: int,
        filter_pattern: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        try:
            params = {
                "logGroupName": log_group_name,
                "startTime": start_time,
                "endTime": end_time,
            }
            if filter_pattern:
                params["filterPattern"] = filter_pattern

            response = self.cloudwatch_logs_client.filter_log_events(**params)
            return response.get("events", [])
        except ClientError as e:
            print(f"Error filtering log events: {e}")
            raise

    def get_query_results(self, query_id: str) -> Dict[str, Any]:
        try:
            response = self.cloudwatch_logs_client.get_query_results(queryId=query_id)
            return response
        except ClientError as e:
            print(f"Error getting query results: {e}")
            raise

    def start_query(
        self, log_group_name: str, start_time: int, end_time: int, query_string: str
    ) -> str:
        try:
            response = self.cloudwatch_logs_client.start_query(
                logGroupName=log_group_name,
                startTime=start_time,
                endTime=end_time,
                queryString=query_string,
                limit=100,  # Example limit
            )
            return response["queryId"]
        except ClientError as e:
            print(f"Error starting query: {e}")
            raise

    def invoke_bedrock_model(
        self, model_id: str, body: Dict[str, Any]
    ) -> Dict[str, Any]:
        import json

        try:
            response = self.bedrock_runtime_client.invoke_model(
                body=json.dumps(body),
                modelId=model_id,
                accept="application/json",
                contentType="application/json",
            )
            response_body = json.loads(response.get("body").read())
            return response_body
        except ClientError as e:
            print(f"Error invoking Bedrock model: {e}")
            raise

    def detect_sentiment(self, text: str, language_code: str = "en") -> Dict[str, Any]:
        try:
            response = self.comprehend_client.detect_sentiment(
                Text=text, LanguageCode=language_code
            )
            return response
        except ClientError as e:
            print(f"Error detecting sentiment with Comprehend: {e}")
            raise

    def translate_text(
        self, text: str, source_language_code: str, target_language_code: str
    ) -> Dict[str, Any]:
        try:
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code,
            )
            return response
        except ClientError as e:
            print(f"Error translating text: {e}")
            raise

    def get_bedrock_embedding(self, text: str) -> List[float]:
        import json

        try:
            body = json.dumps({"inputText": text})
            response = self.bedrock_runtime_client.invoke_model(
                body=body,
                modelId="amazon.titan-embed-text-v1",  # Amazon Titan Embeddings
                accept="application/json",
                contentType="application/json",
            )
            response_body = json.loads(response.get("body").read())
            return response_body["embedding"]
        except ClientError as e:
            print(f"Error getting Bedrock embedding: {e}")
            raise

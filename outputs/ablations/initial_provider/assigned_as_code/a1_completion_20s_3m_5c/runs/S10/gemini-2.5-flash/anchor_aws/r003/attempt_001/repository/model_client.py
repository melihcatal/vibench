import boto3
import os
from typing import Dict, Any, List, Optional
from model_models import ConverseRequest, ConverseResponse, Message

class BedrockClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region_name)

    def converse(self, request: ConverseRequest) -> ConverseResponse:
        messages_payload = []
        for msg in request.messages:
            content_list = []
            for item in msg.content:
                if 'text' in item:
                    content_list.append({"text": item['text']})
                elif 'image' in item:
                    content_list.append({"image": item['image']})
            messages_payload.append({"role": msg.role, "content": content_list})

        inference_config = {}
        if request.max_tokens is not None:
            inference_config["maxTokens"] = request.max_tokens
        if request.temperature is not None:
            inference_config["temperature"] = request.temperature
        if request.top_p is not None:
            inference_config["topP"] = request.top_p
        
        body = {
            "modelId": request.model_id,
            "messages": messages_payload,
        }

        if inference_config:
            body["inferenceConfig"] = inference_config

        response = self.client.converse(
            **body
        )

        text = "".join(
            block["text"]
            for block in response["output"]["message"]["content"]
            if "text" in block
        )

        stop_reason = None
        if "stopReason" in response["output"]["message"]["stopReason"]:
            stop_reason = response["output"]["message"]["stopReason"]

        return ConverseResponse(
            text=text,
            stop_reason=stop_reason,
            input_tokens=response["usage"]["inputTokens"],
            output_tokens=response["usage"]["outputTokens"],
        )

    def converse_stream(self, request: ConverseRequest):
        messages_payload = []
        for msg in request.messages:
            content_list = []
            for item in msg.content:
                if 'text' in item:
                    content_list.append({"text": item['text']})
                elif 'image' in item:
                    content_list.append({"image": item['image']})
            messages_payload.append({"role": msg.role, "content": content_list})

        inference_config = {}
        if request.max_tokens is not None:
            inference_config["maxTokens"] = request.max_tokens
        if request.temperature is not None:
            inference_config["temperature"] = request.temperature
        if request.top_p is not None:
            inference_config["topP"] = request.top_p
        
        body = {
            "modelId": request.model_id,
            "messages": messages_payload,
        }

        if inference_config:
            body["inferenceConfig"] = inference_config

        response = self.client.converse_stream(
            **body
        )
        
        for event in response["stream"]:
            if "contentBlockDelta" in event:
                for block in event["contentBlockDelta"]["delta"]["text"]:
                    yield block
            elif "messageStop" in event:
                yield {"stop_reason": event["messageStop"]["stopReason"]}
            elif "metadata" in event:
                yield {
                    "input_tokens": event["metadata"]["usage"]["inputTokens"],
                    "output_tokens": event["metadata"]["usage"]["outputTokens"],
                }


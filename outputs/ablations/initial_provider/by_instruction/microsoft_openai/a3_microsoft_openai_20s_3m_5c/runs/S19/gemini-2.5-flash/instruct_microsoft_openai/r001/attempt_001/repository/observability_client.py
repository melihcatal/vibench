import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import openai
import json

# Azure Monitor Imports
from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError
from azure.monitor.query import MetricAggregationType

# Google Cloud Monitoring Imports
from google.cloud import monitoring_v3
from google.api import metric_pb2, monitored_resource_pb2
from google.protobuf.duration_pb2 import Duration

# AWS CloudWatch Imports
import boto3
from botocore.exceptions import ClientError

# Google Cloud Translation Imports
from google.cloud import translate

# Google Cloud Perspective API Imports
from google.cloud import commentanalyzer_v1beta1 as commentanalyzer
from google.cloud.commentanalyzer_v1beta1 import types

from observability_models import MetricQueryRequest, MetricQueryResponse, MetricDataPoint

class ObservabilityClient:
    def query_metric_window(self, request: MetricQueryRequest) -> MetricQueryResponse:
        raise NotImplementedError

    def aggregate_metric_stats(self, request: MetricQueryRequest, resource_id: str, aggregations: List[str]) -> Dict[str, Any]:
        raise NotImplementedError
    
    def filter_metric_dimensions(self, request: MetricQueryRequest, project_id: str) -> MetricQueryResponse:
        raise NotImplementedError
    
    def compare_metric_series(self, request1: MetricQueryRequest, request2: MetricQueryRequest) -> Dict[str, Any]:
        raise NotImplementedError

    def summarize_metrics(self, metric_data: MetricQueryResponse, prompt_text: Optional[str] = None) -> str:
        raise NotImplementedError
    
    def check_annotation_safety(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError
    
    def translate_text(self, text: str, target_language: str, project_id: str) -> str:
        raise NotImplementedError
    
    def archive_metric_snapshot(self, bucket_name: str, file_name: str, content: str, region_name: str) -> Dict[str, Any]:
        raise NotImplementedError


class OpenAIMetricsClient(ObservabilityClient):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def query_metric_window(self, request: MetricQueryRequest) -> MetricQueryResponse:
        prompt = f"""Generate a JSON object representing metric data points for the metric '{request.metric_name}' from {request.start_time.isoformat()} to {request.end_time.isoformat()}. 
        Include approximately 10 data points with a timestamp and a float value. The timestamps should be monotonically increasing within the window.
        If dimensions are provided: {request.dimensions_filter}, include them in each datapoint. Provide a unit if appropriate, for example, 'count' or 'milliseconds'.
        Example format: {{\"metric_name\": \"cpu_usage\", \"unit\": \"percent\", \"data_points\": [{{\"timestamp\": \"2023-01-01T00:00:00Z\", \"value\": 50.5, \"dimensions\": {{\"host\": \"server1\"}}}}...]}}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."}, 
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        
        if content:
            try:
                json_response = json.loads(content)
                data_points = []
                for dp in json_response.get("data_points", []):
                    data_points.append(MetricDataPoint(
                        timestamp=datetime.fromisoformat(dp["timestamp"].replace('Z', '+00:00')),
                        value=float(dp["value"]),
                        dimensions=dp.get("dimensions")
                    ))
                return MetricQueryResponse(
                    metric_name=json_response.get("metric_name", request.metric_name),
                    data_points=data_points,
                    unit=json_response.get("unit"),
                    resource_id=json_response.get("resource_id")
                )
            except json.JSONDecodeError:
                print(f"Error decoding JSON from OpenAI: {content}")
                return MetricQueryResponse(metric_name=request.metric_name, data_points=[])
        return MetricQueryResponse(metric_name=request.metric_name, data_points=[])

    def summarize_metrics(self, metric_data: MetricQueryResponse, prompt_text: Optional[str] = None) -> str:
        data_points_str = json.dumps([{"timestamp": dp.timestamp.isoformat(), "value": dp.value, "dimensions": dp.dimensions} for dp in metric_data.data_points], indent=2)
        
        if prompt_text is None:
            prompt_text = f"Summarize the following metric data for '{metric_data.metric_name}'. Identify any trends, anomalies, or interesting observations. The data is:\n{data_points_str}"
        else:
            prompt_text = f"{prompt_text}\n\nMetric Data for '{metric_data.metric_name}':\n{data_points_str}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes metric data and identifies trends or anomalies."}, 
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content or "No summary generated."


class AzureMonitorMetricsClient(ObservabilityClient):
    def __init__(self, subscription_id: str):
        self.credential = DefaultAzureCredential()
        self.client = MetricsQueryClient(self.credential)
        self.subscription_id = subscription_id

    def aggregate_metric_stats(self, request: MetricQueryRequest, resource_id: str, aggregations: List[str]) -> Dict[str, Any]:
        try:
            timespan = f"{request.start_time.isoformat()}/{request.end_time.isoformat()}"
            
            azure_aggregations = []
            for agg in aggregations:
                if agg.lower() == "average":
                    azure_aggregations.append(MetricAggregationType.AVERAGE)
                elif agg.lower() == "count":
                    azure_aggregations.append(MetricAggregationType.COUNT)
                elif agg.lower() == "maximum":
                    azure_aggregations.append(MetricAggregationType.MAXIMUM)
                elif agg.lower() == "minimum":
                    azure_aggregations.append(MetricAggregationType.MINIMUM)
                elif agg.lower() == "total":
                    azure_aggregations.append(MetricAggregationType.TOTAL)

            metrics_response = self.client.query_resource(
                resource_id=resource_id,
                metric_names=[request.metric_name],
                timespan=timespan,
                interval=request.interval, 
                aggregations=azure_aggregations
            )

            result = {
                "metric_name": request.metric_name,
                "start_time": request.start_time.isoformat(),
                "end_time": request.end_time.isoformat(),
                "interval": request.interval,
                "aggregations_requested": aggregations,
                "timeseries_data": []
            }

            for metric in metrics_response.metrics:
                for time_series in metric.timeseries:
                    for data_point in time_series.data:
                        dp_values = {}
                        for agg_type in azure_aggregations:
                            val = getattr(data_point, agg_type.value.lower(), None)
                            if val is not None:
                                dp_values[agg_type.value] = val
                        
                        result["timeseries_data"].append({
                            "timestamp": data_point.timestamp.isoformat(),
                            "values": dp_values,
                            "dimensions": {d.name: d.value for d in time_series.metadata} if time_series.metadata else {} 
                        })

            return result

        except HttpResponseError as e:
            print(f"Error querying Azure Monitor: {e.message}")
            return {"error": str(e)}
        except Exception as e:
            print(f"An unexpected error occurred with Azure Monitor: {e}")
            return {"error": str(e)}


class GoogleCloudMetricsClient(ObservabilityClient):
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()

    def filter_metric_dimensions(self, request: MetricQueryRequest, project_id: str) -> MetricQueryResponse:
        project_name = f"projects/{project_id}"
        
        interval = monitoring_v3.TimeInterval()
        interval.end_time.FromDatetime(request.end_time)
        interval.start_time.FromDatetime(request.start_time)

        # Default alignment_period if interval is not provided in the request
        alignment_period_seconds = int((request.end_time - request.start_time).total_seconds() / 10) if request.interval is None else None
        if request.interval and request.interval.startswith("PT") and request.interval.endswith("M"): # Example: PT5M
            alignment_period_seconds = int(request.interval[2:-1]) * 60
        elif request.interval and request.interval.startswith("PT") and request.interval.endswith("H"): # Example: PT1H
            alignment_period_seconds = int(request.interval[2:-1]) * 3600
        
        aggregation_pb = monitoring_v3.Aggregation(
            alignment_period=Duration(seconds=alignment_period_seconds) if alignment_period_seconds else None,
            per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        )

        # Build the filter string
        metric_type = request.metric_name # Assuming metric_name here is the full metric type for Google Cloud
        filter_str = f"metric.type = \"{metric_type}\""
        
        if request.dimensions_filter:
            for dim_key, dim_value in request.dimensions_filter.items():
                # Google Cloud Monitoring labels can be metric.labels.<key> or resource.labels.<key>
                # For simplicity, trying metric.labels first, can be extended for resource.labels.
                filter_str += f" AND metric.labels.\"{dim_key}\" = \"{dim_value}\""
                aggregation_pb.group_by_fields.append(f"metric.labels.\"{dim_key}\"")

        query_results = self.client.list_time_series(
            name=project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=aggregation_pb
        )

        data_points = []
        for ts in query_results:
            for point in ts.points:
                # Determine the value type (double, int64, string, bool)
                value = None
                if point.value.HasField("double_value"): value = point.value.double_value
                elif point.value.HasField("int64_value"): value = point.value.int64_value
                elif point.value.HasField("string_value"): value = point.value.string_value
                elif point.value.HasField("bool_value"): value = point.value.bool_value

                data_points.append(MetricDataPoint(
                    timestamp=point.interval.end_time.ToDatetime(),
                    value=value,
                    dimensions=dict(ts.metric.labels) # Or resource.labels depending on context
                ))
        
        return MetricQueryResponse(
            metric_name=request.metric_name,
            data_points=data_points
        )


class AWSCloudWatchMetricsClient(ObservabilityClient):
    def __init__(self, region_name: str):
        self.client = boto3.client("cloudwatch", region_name=region_name)

    def _get_metric_data(self, request: MetricQueryRequest, id_suffix: str) -> Dict[str, Any]:
        metric_data_queries = [
            {
                "Id": f"m{id_suffix}",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2", # Example namespace, should be dynamic or configured
                        "MetricName": request.metric_name,
                        "Dimensions": [{
                            "Name": k, 
                            "Value": v
                        } for k, v in request.dimensions_filter.items()] if request.dimensions_filter else []
                    },
                    "Period": 300, # Default to 5 minutes
                    "Stat": "Average" # Default stat
                },
                "ReturnData": True,
            }
        ]
        
        # Attempt to parse interval into seconds for Period
        period = 300 # Default to 5 minutes
        if request.interval:
            try:
                if request.interval.startswith("PT") and request.interval.endswith("M"):
                    period = int(request.interval[2:-1]) * 60
                elif request.interval.startswith("PT") and request.interval.endswith("H"):
                    period = int(request.interval[2:-1]) * 3600
            except ValueError:
                pass
        
        metric_data_queries[0]["MetricStat"]["Period"] = period

        try:
            response = self.client.get_metric_data(
                MetricDataQueries=metric_data_queries,
                StartTime=request.start_time,
                EndTime=request.end_time,
                ScanBy='TimestampAscending'
            )
            return response
        except ClientError as e:
            print(f"Error fetching metric data from CloudWatch: {e}")
            return {"error": str(e)}

    def compare_metric_series(self, request1: MetricQueryRequest, request2: MetricQueryRequest) -> Dict[str, Any]:
        response1 = self._get_metric_data(request1, "1")
        response2 = self._get_metric_data(request2, "2")

        comparison_result = {
            "metric_name": request1.metric_name, # Assuming same metric name for comparison
            "series1": [],
            "series2": [],
            "comparison_details": ""
        }

        if "MetricDataResults" in response1 and response1["MetricDataResults"]:
            for result in response1["MetricDataResults"]:
                for i in range(len(result.get("Timestamps", []))):
                    comparison_result["series1"].append({
                        "timestamp": result["Timestamps"][i].isoformat(),
                        "value": result["Values"][i]
                    })
        
        if "MetricDataResults" in response2 and response2["MetricDataResults"]:
            for result in response2["MetricDataResults"]:
                for i in range(len(result.get("Timestamps", []))):
                    comparison_result["series2"].append({
                        "timestamp": result["Timestamps"][i].isoformat(),
                        "value": result["Values"][i]
                    })

        # Simple comparison logic (can be expanded)
        if len(comparison_result["series1"]) > 0 and len(comparison_result["series2"]) > 0:
            avg1 = sum(dp["value"] for dp in comparison_result["series1"]) / len(comparison_result["series1"])
            avg2 = sum(dp["value"] for dp in comparison_result["series2"]) / len(comparison_result["series2"])
            comparison_result["comparison_details"] = f"Average for Series 1: {avg1:.2f}, Average for Series 2: {avg2:.2f}. "
            if avg1 > avg2:
                comparison_result["comparison_details"] += "Series 1 has a higher average value."
            elif avg2 > avg1:
                comparison_result["comparison_details"] += "Series 2 has a higher average value."
            else:
                comparison_result["comparison_details"] += "Series 1 and Series 2 have similar average values."
        else:
            comparison_result["comparison_details"] = "Not enough data to perform a meaningful comparison."

        return comparison_result


class PerspectiveAPIClient(ObservabilityClient):
    def __init__(self):
        self.client = commentanalyzer.CommentAnalyzerClient()

    def check_annotation_safety(self, text: str) -> Dict[str, Any]:
        analyze_request = types.AnalyzeCommentRequest({
            'comment': {'text': text},
            'requested_attributes': {
                'TOXICITY': {},
                'PROFANITY': {},
                'THREAT': {},
                'INSULT': {},
                'FLIRTATION': {}
            }
        })
        response = self.client.analyze_comment(request=analyze_request)

        result = {
            "text": text,
            "scores": {},
            "is_unsafe": False
        }

        for attribute, score in response.attribute_scores.items():
            result["scores"][attribute] = score.summary_score.value
        
        # Define a threshold for safety. These values can be tuned.
        # If any attribute score exceeds a threshold, consider it unsafe.
        UNSAFE_THRESHOLD = 0.7 # Example threshold
        for score_value in result["scores"].values():
            if score_value > UNSAFE_THRESHOLD:
                result["is_unsafe"] = True
                break
            
        return result


class GoogleTranslateClient(ObservabilityClient):
    def __init__(self):
        self.client = translate.TranslationServiceClient()

    def translate_text(self, text: str, target_language: str, project_id: str) -> str:
        parent = f"projects/{project_id}"
        response = self.client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        return response.translations[0].translated_text


class AWSS3Client(ObservabilityClient):
    def __init__(self, region_name: str):
        self.client = boto3.client("s3", region_name=region_name)

    def archive_metric_snapshot(self, bucket_name: str, file_name: str, content: str, region_name: str) -> Dict[str, Any]:
        try:
            self.client.put_object(Bucket=bucket_name, Key=file_name, Body=content)
            return {"status": "success", "bucket": bucket_name, "key": file_name, "location": f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{file_name}"}
        except ClientError as e:
            print(f"Error archiving to S3: {e}")
            return {"status": "error", "message": str(e)}

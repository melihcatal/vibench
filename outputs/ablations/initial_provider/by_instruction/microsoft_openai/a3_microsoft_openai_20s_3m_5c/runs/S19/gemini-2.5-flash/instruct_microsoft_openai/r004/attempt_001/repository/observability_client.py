import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

import openai
import boto3
from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential
from google.cloud import monitoring_v3
from google.cloud import translate
from google.cloud import storage
import google.generativeai as genai
# Assuming azure-ai-contentsafety is installed or using a direct REST call for brevity

from observability_models import (
    MetricWindowResponse,
    MetricDataPoint,
    MetricAggregationResponse,
    MetricDimensionFilterResponse,
    MetricComparisonResponse,
    MetricSummary,
    AnnotationSafetyResult,
    TranslatedText,
    ArchivedMetricSnapshot,
    MetricQuery
)

class ObservabilityClient:
    def __init__(
        self, 
        openai_api_key: str,
        azure_subscription_id: str = None,
        aws_region: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        google_project_id: str = None,
        google_gemini_api_key: str = None,
        azure_content_safety_endpoint: str = None,
        azure_content_safety_key: str = None,
    ):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        self.azure_monitor_client = None
        if azure_subscription_id:
            try:
                credential = DefaultAzureCredential()
                self.azure_monitor_client = MetricsQueryClient(credential=credential)
                self.azure_subscription_id = azure_subscription_id
            except Exception as e:
                print(f"Could not initialize Azure Monitor client: {e}")

        self.aws_cloudwatch_client = None
        self.aws_s3_client = None
        if aws_region and aws_access_key_id and aws_secret_access_key:
            try:
                session = boto3.Session(
                    region_name=aws_region,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key
                )
                self.aws_cloudwatch_client = session.client("cloudwatch")
                self.aws_s3_client = session.client("s3")
            except Exception as e:
                print(f"Could not initialize AWS clients: {e}")
        
        self.google_monitoring_client = None
        self.google_translate_client = None
        self.google_storage_client = None # Using this for the archive
        if google_project_id:
            try:
                self.google_monitoring_client = monitoring_v3.MetricServiceClient()
                self.google_translate_client = translate.TranslationServiceClient()
                self.google_storage_client = storage.Client(project=google_project_id)
                self.google_project_id = google_project_id
            except Exception as e:
                print(f"Could not initialize Google Cloud clients: {e}")
        
        self.google_gemini_client = None
        if google_gemini_api_key:
            try:
                genai.configure(api_key=google_gemini_api_key)
                self.google_gemini_client = genai.GenerativeModel('gemini-pro') # Concrete model identifier
            except Exception as e:
                print(f"Could not initialize Google Gemini client: {e}")

        self.azure_content_safety_endpoint = azure_content_safety_endpoint
        self.azure_content_safety_key = azure_content_safety_key


    def query_openai_metric_window(self, metric_name: str, start_time: datetime, end_time: datetime) -> MetricWindowResponse:
        prompt = (
            f"Generate a list of simulated metric data points for '{metric_name}' "
            f"between {start_time.isoformat()} and {end_time.isoformat()}. "
            "Provide 5 data points with timestamps and float values. "
            "Format as a JSON string with 'metric_name' and 'data_points' (list of {'timestamp': 'ISO_FORMAT', 'value': float})."
        )
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Concrete model identifier
            messages=[
                {"role": "system", "content": "You are a metric data simulator."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("No content received from OpenAI.")
        json_response = json.loads(content)

        data_points = []
        for dp in json_response.get("data_points", []):
            try:
                data_points.append(MetricDataPoint(
                    timestamp=datetime.fromisoformat(dp['timestamp']),
                    value=float(dp['value'])
                ))
            except (KeyError, ValueError) as e:
                print(f"Skipping malformed data point: {dp} - {e}")
        
        return MetricWindowResponse(
            metric_name=json_response.get("metric_name", metric_name),
            data_points=data_points
        )

    def get_azure_monitor_aggregated_metric_stats(self, resource_id: str, metric_name: str, start_time: datetime, end_time: datetime, aggregation: str) -> MetricAggregationResponse:
        if not self.azure_monitor_client:
            raise RuntimeError("Azure Monitor client not initialized.")
        
        # Azure Monitor expects aggregation as a comma-separated string, e.g., "Average,Total"
        # We'll simplify for this example to a single aggregation type
        timespan = f"{start_time.isoformat()}/{end_time.isoformat()}"
        
        metrics_response = self.azure_monitor_client.query_resource(
            resource_id=resource_id,
            metric_names=[metric_name],
            timespan=timespan,
            aggregations=[aggregation] # e.g., "Average", "Total"
        )
        
        value = 0.0
        # Iterate over the response to extract the aggregated value
        for metric in metrics_response.metrics:
            for time_series in metric.timeseries:
                for data in time_series.data:
                    if hasattr(data, aggregation.lower()) and getattr(data, aggregation.lower()) is not None:
                        value = getattr(data, aggregation.lower())
                        break # Assuming one value per aggregation for simplicity
            if value != 0.0:
                break

        return MetricAggregationResponse(
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
            statistic=aggregation,
            value=value
        )

    def get_cloudwatch_filtered_metric_dimensions(self, namespace: str, metric_name: str, start_time: datetime, end_time: datetime, dimensions: Dict[str, str]) -> MetricDimensionFilterResponse:
        if not self.aws_cloudwatch_client:
            raise RuntimeError("AWS CloudWatch client not initialized.")

        cloudwatch_dimensions = [{'Name': k, 'Value': v} for k, v in dimensions.items()]

        response = self.aws_cloudwatch_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name,
                            'Dimensions': cloudwatch_dimensions
                        },
                        'Period': 300, # 5 minutes
                        'Stat': 'Average'
                    },
                    'ReturnData': True,
                },
            ],
            StartTime=start_time,
            EndTime=end_time
        )

        filtered_data_points: Dict[str, List[MetricDataPoint]] = {}
        # CloudWatch returns data points in reverse chronological order
        for metric_data_result in response.get('MetricDataResults', []):
            id_key = metric_data_result.get('Id', 'default')
            data_points = []
            for i in range(len(metric_data_result.get('Timestamps', []))):
                timestamp = metric_data_result['Timestamps'][i]
                value = metric_data_result['Values'][i]
                data_points.append(MetricDataPoint(timestamp=timestamp, value=value))
            filtered_data_points[id_key] = sorted(data_points, key=lambda dp: dp.timestamp)

        return MetricDimensionFilterResponse(
            metric_name=metric_name,
            filtered_data_points=filtered_data_points
        )

    def get_google_cloud_monitoring_metric_series(self, project_id: str, metric_type: str, filter_a: str, filter_b: str, start_time: datetime, end_time: datetime) -> MetricComparisonResponse:
        if not self.google_monitoring_client:
            raise RuntimeError("Google Cloud Monitoring client not initialized.")

        interval = monitoring_v3.TimeInterval(
            end_time=end_time.isoformat(timespec='seconds') + 'Z',
            start_time=start_time.isoformat(timespec='seconds') + 'Z'
        )
        
        # Helper to fetch time series for a given filter
        def fetch_time_series(filter_str: str) -> List[MetricDataPoint]:
            query_filter = f"metric.type = \"{metric_type}\" AND {filter_str}"
            result = self.google_monitoring_client.list_time_series(
                name=f"projects/{project_id}",
                filter=query_filter,
                interval=interval,
                view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            )
            
            data_points = []
            for series in result:
                for point in series.points:
                    # Google Monitoring returns value as a TypedValue, need to extract the actual value
                    value = getattr(point.value, point.value.WhichOneof("value_type"))
                    data_points.append(MetricDataPoint(
                        timestamp=point.interval.end_time.replace(tzinfo=None), # Convert to naive datetime
                        value=float(value)
                    ))
            return sorted(data_points, key=lambda dp: dp.timestamp)

        resource_a_data_points = fetch_time_series(filter_a)
        resource_b_data_points = fetch_time_series(filter_b)

        return MetricComparisonResponse(
            metric_name=metric_type.split('/')[-1] if '/' in metric_type else metric_type, # Extract short name
            resource_a_data_points=resource_a_data_points,
            resource_b_data_points=resource_b_data_points
        )

    def summarize_metric_trends_gemini(self, metric_name: str, data_points: List[MetricDataPoint]) -> MetricSummary:
        if not self.google_gemini_client:
            raise RuntimeError("Google Gemini client not initialized.")
        
        # Prepare a simple text representation of data points for the LLM
        data_summary = "\n".join([f"  {dp.timestamp}: {dp.value}" for dp in data_points])
        prompt = (
            f"Given the following data points for metric '{metric_name}':\n"
            f"{data_summary}\n\n"
            "Summarize the recent trends or anomalies observed in this metric."
        )

        response = self.google_gemini_client.generate_content(prompt)
        summary_text = response.text
        
        return MetricSummary(metric_name=metric_name, summary_text=summary_text)

    def check_azure_content_safety(self, text: str) -> AnnotationSafetyResult:
        if not self.azure_content_safety_endpoint or not self.azure_content_safety_key:
            raise RuntimeError("Azure Content Safety client not configured.")

        import requests
        headers = {
            'Ocp-Apim-Subscription-Key': self.azure_content_safety_key,
            'Content-Type': 'application/json'
        }
        json_data = {
            'text': text,
            'categories': ["Hate", "Sexual", "SelfHarm", "Violence"],
            'blocklistNames': []
        }
        
        # Concrete API endpoint
        url = f"{self.azure_content_safety_endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"

        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        result = response.json()

        is_safe = True
        reasons = []

        # Check for severities in categories
        for category in result.get('categoriesAnalysis', []):
            if category.get('severity', 0) > 0:
                is_safe = False
                reasons.append(f"Content violates category: {category.get('category')} with severity {category.get('severity')}")
        
        return AnnotationSafetyResult(text=text, is_safe=is_safe, reasons=reasons)


    def translate_google_cloud_text(self, text: str, target_locale: str, project_id: str) -> TranslatedText:
        if not self.google_translate_client:
            raise RuntimeError("Google Cloud Translation client not initialized.")

        parent = f"projects/{project_id}/locations/global"

        response = self.google_translate_client.translate_text(
            parent=parent,
            contents=[text],
            target_language_code=target_locale,
            mime_type="text/plain",  # Mime types: "text/plain" or "text/html"
        )

        translated_text = ""
        for translation in response.translations:
            translated_text += translation.translated_text
        
        return TranslatedText(
            original_text=text,
            translated_text=translated_text,
            target_locale=target_locale
        )

    def archive_s3_metric_snapshot(self, bucket_name: str, object_key: str, snapshot_data: str) -> ArchivedMetricSnapshot:
        if not self.aws_s3_client:
            raise RuntimeError("AWS S3 client not initialized.")
        
        self.aws_s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=snapshot_data
        )

        s3_url = f"s3://{bucket_name}/{object_key}"
        return ArchivedMetricSnapshot(snapshot_id=object_key, storage_url=s3_url, timestamp=datetime.now())

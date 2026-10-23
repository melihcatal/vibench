import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest

def retrieve_aggregated_stats(property_id, metric_name, start_date, end_date):
    client = BetaAnalyticsDataClient()
    date_range = DateRange(start_date=start_date, end_date=end_date)
    metric = Metric(name=metric_name)
    request = RunReportRequest(
        property=f'properties/{property_id}',
        date_ranges=[date_range],
        metrics=[metric]
    )
    response = client.run_report(request)
    return response.rows[0].metric_values[0].value if response.rows else None

if __name__ == '__main__':
    property_id = 'YOUR_PROPERTY_ID'
    metric_name = 'activeUsers'
    start_date = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    end_date = datetime.date.today().isoformat()
    result = retrieve_aggregated_stats(property_id, metric_name, start_date, end_date)
    print(f'Aggregated {metric_name} over the last 30 days: {result}')

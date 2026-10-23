from google.analytics.data import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest

def get_aggregated_metric_stats(property_id, metric_name, start_date, end_date):
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f'properties/{property_id}',
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        metrics=[Metric(name=metric_name)]
    )
    response = client.run_report(request)
    return response.rows

if __name__ == '__main__':
    property_id = 'YOUR_PROPERTY_ID'
    metric_name = 'activeUsers'
    start_date = '2023-01-01'
    end_date = '2023-01-31'
    stats = get_aggregated_metric_stats(property_id, metric_name, start_date, end_date)
    for row in stats:
        print(row)
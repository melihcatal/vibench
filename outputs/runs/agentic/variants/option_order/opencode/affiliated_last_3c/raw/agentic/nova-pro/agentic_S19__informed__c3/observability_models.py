from google.cloud import monitoring_v3


# Helper function to parse time series
def parse_time_series(time_series):
    parsed_data = []
    for series in time_series:
        for point in series.points:
            parsed_data.append(
                {"value": point.value.double_value, "time": point.interval.end_time}
            )
    return parsed_data

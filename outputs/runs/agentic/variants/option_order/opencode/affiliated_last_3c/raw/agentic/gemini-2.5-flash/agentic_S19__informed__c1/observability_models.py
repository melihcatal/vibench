import datetime


def normalize_time_series(time_series_data):
    # Placeholder for actual normalization logic
    normalized_data = []
    for ts in time_series_data:
        for point in ts.points:
            normalized_data.append(
                {
                    "value": point.value.double_value or point.value.int64_value,
                    "timestamp": point.interval.end_time.isoformat(),
                }
            )
    return normalized_data


def create_time_interval(end_time_str, minutes):
    end_time = datetime.datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))
    start_time = end_time - datetime.timedelta(minutes=minutes)
    return monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

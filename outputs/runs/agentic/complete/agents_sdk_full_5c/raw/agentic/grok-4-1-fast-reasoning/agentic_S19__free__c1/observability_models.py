from typing import List, Dict, Any

def normalize_get_metric_data_result(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    timestamps = result['Timestamps']
    values = result['Values']
    labels = result.get('Labels', [None] * len(values))
    return [
        {
            'timestamp': ts.isoformat() if hasattr(ts, 'isoformat') else str(ts),
            'value': val,
            'label': label
        }
        for ts, val, label in zip(timestamps, values, labels)
    ]

def normalize_get_metric_statistics_datapoints(datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for dp in datapoints:
        norm_dp = {'timestamp': str(dp['Timestamp'])}
        for key in ['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum', 'Unit']:
            if key in dp:
                norm_dp[key.lower()] = dp[key]
        normalized.append(norm_dp)
    return normalized

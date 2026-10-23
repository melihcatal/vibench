from typing import List, Dict, Any


def normalize_datapoints(datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for dp in datapoints:
        norm_dp = {
            "timestamp": dp["Timestamp"],
            "value": dp["Average"],
        }
        if "Maximum" in dp:
            norm_dp["max"] = dp["Maximum"]
        if "Minimum" in dp:
            norm_dp["min"] = dp["Minimum"]
        if "Sum" in dp:
            norm_dp["sum"] = dp["Sum"]
        norm_dp["sample_count"] = dp.get("SampleCount", 0)
        norm_dp["unit"] = dp.get("Unit", "")
        normalized.append(norm_dp)
    return normalized

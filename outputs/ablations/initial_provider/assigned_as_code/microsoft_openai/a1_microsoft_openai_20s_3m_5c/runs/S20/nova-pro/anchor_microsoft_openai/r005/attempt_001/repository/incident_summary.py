from observability_models import parse_log_response


def incident_summary(logs):
    summarized_logs = parse_log_response(logs)
    return {'summary': summarized_logs}
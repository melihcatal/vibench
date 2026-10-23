import datetime
from security_client import SecurityClientConfig
from security_models import KeyUsageSummary

def get_kms_key_usage_summary(
    start_time: datetime.datetime,
    end_time: datetime.datetime
) -> KeyUsageSummary:
    cloudtrail_client = SecurityClientConfig.get_cloudtrail_client()

    paginator = cloudtrail_client.get_paginator('lookup_events')
    
    total_kms_events = 0
    encrypt_calls = 0
    decrypt_calls = 0
    generate_data_key_calls = 0
    sign_calls = 0
    verify_calls = 0
    other_kms_events = 0

    response_iterator = paginator.paginate(
        LookupAttributes=[
            {'AttributeKey': 'EventSource', 'AttributeValue': 'kms.amazonaws.com'}
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    for page in response_iterator:
        for event_dict in page.get('Events', []):
            total_kms_events += 1
            event_name = event_dict.get('EventName')
            
            if event_name == 'Encrypt':
                encrypt_calls += 1
            elif event_name == 'Decrypt':
                decrypt_calls += 1
            elif event_name == 'GenerateDataKey' or event_name == 'GenerateDataKeyWithoutPlaintext':
                generate_data_key_calls += 1
            elif event_name == 'Sign':
                sign_calls += 1
            elif event_name == 'Verify':
                verify_calls += 1
            else:
                other_kms_events += 1

    return KeyUsageSummary(
        total_kms_events=total_kms_events,
        encrypt_calls=encrypt_calls,
        decrypt_calls=decrypt_calls,
        generate_data_key_calls=generate_data_key_calls,
        sign_calls=sign_calls,
        verify_calls=verify_calls,
        other_kms_events=other_kms_events
    )
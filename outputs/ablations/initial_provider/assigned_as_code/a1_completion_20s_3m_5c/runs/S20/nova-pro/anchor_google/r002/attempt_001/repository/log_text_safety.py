import boto3

cw_logs = boto3.client('logs', region_name='us-west-2')

def check_log_text_safety(log_text):
    # Placeholder for actual safety check implementation
    return 'safe' if 'ERROR' not in log_text else 'unsafe'

if __name__ == '__main__':
    log_text = 'User login attempt'
    safety_status = check_log_text_safety(log_text)
    print(f'Log text safety status: {safety_status}'
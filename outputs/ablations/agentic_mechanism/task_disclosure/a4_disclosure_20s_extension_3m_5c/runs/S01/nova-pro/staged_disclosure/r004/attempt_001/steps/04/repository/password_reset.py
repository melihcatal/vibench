import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_password_reset_email(to_email, reset_link):
    message = Mail(
        from_email='your-email@example.com',
        to_emails=to_email,
        subject='Password Reset',
        html_content=f'<strong>Click the link to reset your password: {reset_link}</strong>'
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code, response.body, response.headers)
    except Exception as e:
        print(e.message)

def start_password_reset(email):
    reset_link = 'https://example.com/reset-password'  # This should be a real link in a real application
    send_password_reset_email(email, reset_link)

if __name__ == '__main__':
    email = input('Enter your email address: ')
    start_password_reset(email)
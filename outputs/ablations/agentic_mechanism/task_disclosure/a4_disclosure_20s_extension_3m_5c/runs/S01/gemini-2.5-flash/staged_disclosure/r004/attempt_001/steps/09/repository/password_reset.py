import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_password_reset_email(recipient_email, reset_link):
    message = Mail(
        from_email=os.environ.get('SENDGRID_SENDER_EMAIL'),
        to_emails=recipient_email,
        subject='Password Reset Request',
        html_content=f'Please click on the following link to reset your password: <a href="{reset_link}">Reset Password</a>'
    )
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(f"Email sent successfully to {recipient_email}. Status Code: {response.status_code}")
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Example usage:
    # Ensure you have SENDGRID_API_KEY and SENDGRID_SENDER_EMAIL set in your environment variables
    # For example:
    # export SENDGRID_API_KEY='YOUR_SENDGRID_API_KEY'
    # export SENDGRID_SENDER_EMAIL='your_verified_sender_email@example.com'

    # In a real application, recipient_email and reset_link would come from your application logic
    test_recipient_email = 'recipient@example.com' # Replace with a real recipient email for testing
    test_reset_link = 'http://your-app.com/reset-password?token=some_secure_token'

    print(f"Attempting to send password reset email to {test_recipient_email}")
    send_password_reset_email(test_recipient_email, test_reset_link)

import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY").strip("'")

URL = os.getenv("URL").strip("'")


def by_email_update(subject, text):
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{URL}/messages",
            auth=("api", API_KEY),
            data={
                "from": f"ITU Dersçi Admin <itudersciadmin@{URL}>",
                "to": ["[ADMIN_EMAIL]", "Admin"],
                "subject": subject,
                "text": text,
            },
        )

        response.raise_for_status()

        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Email sending failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the email: {e}")


if __name__ == "__main__":
    subject = "Test"
    text = "Test"
    by_email_update(subject, text)

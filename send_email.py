import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv


# SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = ""  # Replace with your email address
PASSWORD = ""  # Replace with your app-specific password (not your regular email password)

# File path to your CSV file
CSV_FILE = "email_list.csv"  # Replace with the path to your CSV file

# Email template with placeholders
EMAIL_BODY_TEMPLATE = """
Hi {name}!<br><br>

Your unique ID<is: <strong>{unique_id}</strong><br><br>
"""

# Function to send an email
def send_email(recipient_email, name, unique_id):
    # Create the email content
    subject = "" # Replace with your subject
    body = EMAIL_BODY_TEMPLATE.format(name=name, unique_id=unique_id)
    
    # Create a MIME email
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient_email, msg.as_string())
        print(f"Email sent to {name} ({recipient_email})")
    except Exception as e:
        print(f"Failed to send email to {name} ({recipient_email}): {e}")

# Read the CSV and send emails
try:
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Automatically maps the header row to keys
        for row in reader:
            name = row["name"]
            email = row["email"]
            unique_id = row["unique_id"]
            send_email(email, name, unique_id)
except FileNotFoundError:
    print(f"File {CSV_FILE} not found.")
except KeyError as e:
    print(f"Missing column in CSV: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

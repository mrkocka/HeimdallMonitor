import smtplib
import requests
import redis
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Kapcsolódás a Redis szerverhez
r = redis.Redis(host='localhost', port=6379, db=0)

# Email küldés beállításai
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "a_gmail_cimed@gmail.com"
GMAIL_PASSWORD = "alkalmazas_jelszo"

def send_email(to_email, subject, body):
    """Email küldése a megadott címre."""
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())
        server.quit()
        print(f"Email elküldve: {to_email}")
    except Exception as e:
        print(f"Hiba történt az email küldésekor: {e}")

def check_website(website_id):
    """Weboldal elérhetőségének ellenőrzése és állapot frissítése Redis-ben."""
    url = r.hget(website_id, "url").decode("utf-8")
    email = r.hget(website_id, "email").decode("utf-8")
    current_status = r.hget(website_id, "allapot").decode("utf-8")

    try:
        # HTTP kérés küldése
        response = requests.get(url, timeout=10)
        new_status = "online" if response.status_code == 200 else "offline"
    except requests.RequestException:
        new_status = "offline"

    # Ha az állapot megváltozott, frissítjük a Redis-ben és küldünk emailt
    if new_status != current_status:
        r.hset(website_id, "allapot", new_status)
        print(f"A(z) {url} állapota megváltozott: {current_status} → {new_status}")

        if new_status == "offline":
            subject = "Weboldal elérhetetlenség figyelmeztetés"
            body = f"A(z) {url} weboldal jelenleg nem elérhető."
            send_email(email, subject, body)

# Weboldalak ellenőrzése
def main():
    website_ids = r.keys("webpage:*")
    for website_id in website_ids:
        check_website(website_id)

if __name__ == "__main__":
    main()
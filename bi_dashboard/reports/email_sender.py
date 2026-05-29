from dataclasses import dataclass
from email.message import EmailMessage
import smtplib


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True


def send_report(config: SMTPConfig, sender: str, recipients: list[str], subject: str, body: str, pdf_bytes: bytes) -> None:
    """Send a generated PDF report through SMTP."""
    message = EmailMessage()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)
    message.add_attachment(pdf_bytes, maintype="application", subtype="pdf", filename="bi_executive_summary.pdf")

    with smtplib.SMTP(config.host, config.port) as server:
        if config.use_tls:
            server.starttls()
        server.login(config.username, config.password)
        server.send_message(message)

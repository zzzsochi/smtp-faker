from collections import namedtuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import smtplib
import sys

try:
    from faker import Faker
except ImportError:
    print("Need to install Faker:")
    print("    pip install Faker")
    sys.exit(1)

HostPort = namedtuple('HostPort', ['host', 'port'])


def send_test_messages(hostport, n):
    for _ in range(n):
        func = random.choice([send_plain, send_html, send_multipart])
        func(hostport)


def send_plain(hostport):
    faker = Faker()

    msg = MIMEText(_fake_plain(faker), 'plain')
    msg['Subject'] = faker.catch_phrase()
    msg['From'] = _fake_email(faker)
    msg['To'] = _fake_email(faker)

    _send(hostport, msg)


def send_html(hostport):
    faker = Faker()

    msg = MIMEText(_fake_html(faker), 'html')
    msg['Subject'] = faker.catch_phrase()
    msg['From'] = _fake_email(faker)
    msg['To'] = _fake_email(faker)

    _send(hostport, msg)


def send_multipart(hostport):
    faker = Faker()

    msg = MIMEMultipart()
    msg['Subject'] = faker.catch_phrase()
    msg['From'] = _fake_email(faker)
    msg['To'] = _fake_email(faker)

    txt = MIMEText(_fake_plain(faker), 'plain')
    msg.attach(txt)

    html = MIMEText(_fake_html(faker), 'html')
    msg.attach(html)

    _send(hostport, msg)


def _fake_email(faker):
    if not faker:
        faker = Faker()

    if random.randint(0, 10) <= 4:
        return '{} <{}>'.format(faker.name(), faker.email())
    else:
        return faker.email()


def _fake_plain(faker):
    return '\n'.join(faker.paragraphs())


def _fake_html(faker):
    tags = [None, 'i', 'b', 'u', 's']
    html = ''
    for src in faker.paragraphs():
        html += '<p>'
        for word in src.split(' '):
            t = random.choice(tags)
            if t:
                html += '<{t}>{w}</{t}> '.format(w=word, t=t)
            else:
                html += word

        html += '</p>\n'

    return html


def _send(hostport, msg):
    smtp = smtplib.SMTP(host=hostport.host, port=hostport.port)
    smtp.sendmail(msg['From'], msg['To'], msg.as_bytes())
    smtp.quit()


def _print_help():
    print("Usage:")
    print("    python3 -m smtp_faker.test N")
    print("    python3 -m smtp_faker.test HOST:PORT N")


if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            hostport = HostPort('localhost', 25)
            n = int(sys.argv[1])
        elif len(sys.argv) == 3:
            host, port = sys.argv[1].split(':', 1)
            hostport = HostPort(host, int(port))
            n = int(sys.argv[2])
        else:
            raise ValueError()

    except ValueError as exc:
        _print_help()
        sys.exit(1)

    send_test_messages(hostport, n)

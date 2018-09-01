from datetime import datetime
from email import message, message_from_bytes
from types import FunctionType
from uuid import uuid1

import aiosmtpd.smtp

from smtp_faker.db import Message


def configure(app, hostport, loop):
    async def message_handler(msg, app=app):
        await app['db'].add(msg)

    smtp_handler = SMTPHandler(message_handler)

    def smtp_factory():
        return aiosmtpd.smtp.SMTP(handler=smtp_handler,
                                  enable_SMTPUTF8=False,
                                  decode_data=False,
                                  hostname='smtp-faker',
                                  loop=loop)

    server = loop.run_until_complete(
        loop.create_server(
            protocol_factory=smtp_factory,
            host=hostport.host,
            port=hostport.port,
        )
    )

    app['smtp_server'] = server
    app.on_shutdown.append(lambda app: server.close())

    print("======== Running SMTP server on {host}:{port} ========".format(
        host=hostport.host,
        port=hostport.port
    ))


class SMTPHandler:
    def __init__(self, message_handler: FunctionType):
        self.message_handler = message_handler

    async def handle_DATA(self, server, session, envelope):
        raw = envelope.content
        msg = await self.create_message(raw)
        await self.message_handler(msg)
        return '250 OK'

    async def create_message(self, raw: bytes) -> Message:
        email = message_from_bytes(raw)
        return Message(
            id=str(uuid1()),
            ts=datetime.utcnow(),
            raw=raw,
            email=email,
            size=len(raw),
            headers=dict(email),
            plain=self._get_plain_email(email),
            html=self._get_html_email(email),
        )

    @staticmethod
    def _get_from_email(email: message.Message, ct: str) -> str:
        def get_from_part(part: message.Message, ct: str) -> str:
            if ct in part.get('Content-Type', ''):
                return part.get_payload()

        payload = email.get_payload()

        if isinstance(payload, str):
            return get_from_part(email, ct)
        else:
            for part in payload:
                res = get_from_part(part, ct)
                if res:
                    return res

    @classmethod
    def _get_plain_email(cls, email: message.Message) -> str:
        text = cls._get_from_email(email, 'text/plain')
        if text is not None:
            return text
        else:
            return email.get_payload() or None

    @classmethod
    def _get_html_email(cls, email: message.Message) -> str:
        return cls._get_from_email(email, 'text/html')

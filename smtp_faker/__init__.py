import asyncio

from aiohttp import web

from . import db, smtpd, static, ws, views


def configure(app, *, size, smtp_hostport, loop):
    app['db'] = db.DB(size=size)

    smtpd.configure(app,
                    hostport=smtp_hostport,
                    loop=loop)

    static.configure(app, loop)

    app.router.add_get('/messages', views.messages)
    app.router.add_get('/messages/{id}', views.message)

    app.router.add_get('/messages/{id}/raw', views.message_raw)
    app.router.add_get('/messages/{id}/plain', views.message_plain)
    app.router.add_get('/messages/{id}/html', views.message_html)

    app.router.add_get('/ws', ws.ws)


def get_application(*, size, smtp_hostport, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    app = web.Application(loop=loop)
    configure(app, size=size, smtp_hostport=smtp_hostport, loop=loop)
    return app

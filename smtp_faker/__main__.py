import argparse
import asyncio
from collections import namedtuple
from functools import partial

from aiohttp import web

from smtp_faker import get_application

DEFAULT_HTTP = 'localhost:8080'
DEFAULT_SMTP = 'localhost:8025'
DEFAULT_SIZE = 10

HostPort = namedtuple('HostPort', ['host', 'port'])


def _parse_hostport(value, default=None):
    if ':' in value:
        host, port = value.split(':', 1)
    elif value.isdigit():
        host = None
        port = int(value)
    else:
        host = value
        port = None

    if host and port:
        return HostPort(host, int(port))
    else:
        default_host, default_port = _parse_hostport(default)
        return HostPort((host or default_host), int(port or default_port))


def _args():
    parser = argparse.ArgumentParser(description='SMTP faker.')

    parser.add_argument('--size', dest='size',
                        default=DEFAULT_SIZE,
                        type=int,
                        metavar='INT',
                        help="size of database (default: {})"
                             "".format(DEFAULT_SIZE))

    parser.add_argument('--http', dest='http_hostport',
                        default=DEFAULT_HTTP,
                        type=partial(_parse_hostport, default=DEFAULT_HTTP),
                        metavar='HOST:PORT',
                        help="listen HTTP host:port")

    parser.add_argument('--smtp', dest='smtp_hostport',
                        default=DEFAULT_SMTP,
                        type=partial(_parse_hostport, default=DEFAULT_SMTP),
                        metavar='HOST:PORT',
                        help="listen SMTP host:port")

    return parser.parse_args()


def main():
    args = _args()
    loop = asyncio.get_event_loop()

    app = get_application(size=args.size,
                          smtp_hostport=args.smtp_hostport,
                          loop=loop)

    web.run_app(app,
                host=args.http_hostport.host,
                port=args.http_hostport.port)


if __name__ == '__main__':
    main()

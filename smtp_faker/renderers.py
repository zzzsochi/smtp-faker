import json

from smtp_faker.db import Message


def _to_iso_datetime(dt):
    return '{:%Y-%m-%d %H:%M:%S}'.format(dt)


def message(msg: Message) -> dict:
    return {
        'id': msg.id,
        'ts': _to_iso_datetime(msg.ts),
        'headers': msg.headers,
        'size': msg.size,
    }


def ws_action_received(msg: Message) -> str:
    return json.dumps({
        'action': 'received',
        'message': message(msg),
    })


def ws_action_removed(msg: Message) -> str:
    return json.dumps({
        'action': 'removed',
        'message': message(msg),
    })


def ws_action_cleared() -> str:
    return json.dumps({
        'action': 'cleared',
    })

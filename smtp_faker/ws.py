import asyncio
import json
from typing import NamedTuple

from aiohttp.web import WebSocketResponse

from smtp_faker import db, renderers


class QItemReceived(NamedTuple):
    action = 'received'
    message: db.Message


class QItemRemoved(NamedTuple):
    action = 'removed'
    message: db.Message


class QItemCleared(NamedTuple):
    action = 'cleared'


class DBListner:
    def __init__(self, db):
        self._db = db

    def __enter__(self) -> asyncio.Queue:
        self._db.listner_add(self)
        self._queue = q = asyncio.Queue(maxsize=1000)
        return q

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._db.listner_remove(self)
        return False

    async def msg_received(self, msg: db.Message):
        await self._queue.put(QItemReceived(message=msg))

    async def msg_removed(self, msg: db.Message):
        await self._queue.put(QItemRemoved(message=msg))

    async def db_cleared(self):
        await self._queue.put(QItemCleared())


async def ws(request):
    ws = WebSocketResponse()
    await ws.prepare(request)

    with DBListner(request.app['db']) as queue:
        while not ws.closed:
            try:
                item = await asyncio.wait_for(queue.get(), 2)
            except asyncio.TimeoutError:
                await ws.ping()
                continue
            except asyncio.CancelledError:
                break
            else:
                if item.action == 'received':
                    await ws.send_str(renderers.ws_action_received(item.message))
                elif item.action == 'removed':
                    await ws.send_str(renderers.ws_action_removed(item.message))
                elif item.action == 'cleared':
                    await ws.send_str(renderers.ws_action_received())
                else:
                    pass

    return ws

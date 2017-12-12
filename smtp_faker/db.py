import asyncio
from datetime import datetime
from email import message_from_bytes
import email.message
import functools
import types
from typing import NamedTuple, Optional, Any, Dict


class Message(NamedTuple):
    id: str
    ts: datetime
    raw: bytes
    email: email.message.Message
    size: int
    headers: Dict[str, str]
    plain: str
    html: str


def _lock(meth: types.MethodType) -> types.MethodType:
    @functools.wraps(meth)
    async def wrapper(self: 'DB', *args, **kwargs) -> Any:
        async with self._locker:
            return await meth(self, *args, **kwargs)

    return wrapper


class DB:
    def __init__(self, size: int):
        self._size = size
        self._inc = 0
        self._data = []
        self._locker = asyncio.Lock()
        self._listners = []

    async def __aiter__(self) -> types.GeneratorType:
        for m in self._data:
            yield m

    @_lock
    async def add(self, msg: Message) -> Message:
        self._data.insert(0, msg)

        if len(self._data) > self._size:
            _removed = self._data.pop(-1)
            for handler in self._listners:
                await handler.msg_removed(_removed)

        for handler in self._listners:
            await handler.msg_received(msg)

        return msg

    async def get(self, _id: str) -> Optional[Message]:
        async for msg in self:
            if msg.id == _id:
                return msg
        else:
            return None

    @_lock
    async def clear(self):
        self._data.clear()

        for handler in self._listners:
            await handler.db_cleared()

    def listner_add(self, handler: '.ws.DBListner'):
        self._listners.append(handler)

    def listner_remove(self, handler: '.ws.DBListner'):
        self._listners.remove(handler)

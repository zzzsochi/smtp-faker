import functools

from aiohttp.web import HTTPNotFound, Response, json_response

from smtp_faker import renderers


async def messages(request):
    db = request.app['db']
    return json_response([renderers.message(m) async for m in db])


def _resolve_message(view):
    @functools.wraps(view)
    async def wrapper(request):
        id = request.match_info['id']

        msg = await request.app['db'].get(id)
        if msg is None:
            raise HTTPNotFound()

        return await view(request, msg)

    return wrapper


@_resolve_message
async def message(request, msg):
    return json_response(renderers.message(msg))


@_resolve_message
async def message_raw(request, msg):
    return Response(body=msg.raw)


@_resolve_message
async def message_plain(request, msg):
    return Response(text=msg.plain, content_type='text/plain')


@_resolve_message
async def message_html(request, msg):
    return Response(text=msg.html, content_type='text/html')

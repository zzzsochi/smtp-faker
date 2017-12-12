import functools
import os
import pkgutil

from aiohttp.web import Response


PREFIX = '/static'


CONTENT_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.ico': 'image/x-icon',
}


def configure(app, loop):
    app.router.add_get(PREFIX + '/{file_name}', static_view)
    app.router.add_get('/', root_view)
    app.router.add_get('/favicon.ico', favicon_view)


def static_view(request):
    return _get_response(request.match_info['file_name'])


def root_view(request):
    return _get_response('index.html')


def favicon_view(request):
    return _get_response('favicon.ico')


def _get_response(file_name):
    path = '/'.join([PREFIX, file_name])
    return Response(
        body=_get_data(path),
        headers={'Content-Type': _get_content_type(file_name)},
    )


@functools.lru_cache(10)
def _get_data(path):
    return pkgutil.get_data('smtp_faker', path)


def _get_content_type(file_name, default='application/octet-stream'):
    ext = os.path.splitext(file_name)[1]
    return CONTENT_TYPES.get(ext, default)

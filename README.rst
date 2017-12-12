==========
SMTP Faker
==========

SMTP server for development.

------------
Installation
------------

Just PIP:

.. code:: bash

    $ pip install smtp-faker
    $ smtp-faker --http=localhost:8080 --smtp=0.0.0.0:8025

Or Docker:

.. code:: bash

    $ docker run --rm -it -p 8080:80 -p 8025:25 zzzsochi/smtp-faker


---
API
---

URLs
----

* `GET /messages`
* `GET /messages/:id`
* `GET /messages/:id/plain`
* `GET /messages/:id/html`
* `GET /messages/:id/raw`
* `/ws`
.. * `POST /messages/:id/forward`

Message object
--------------

:id: str
:ts: ISO-date timestamp
:size: int, size in bytes
:headers: message headers

    :From: sender address
    :To: recievers
    :Subject: message subject

    ...and other headers.

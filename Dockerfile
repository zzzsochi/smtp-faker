FROM alpine
COPY . /srv/src

RUN apk update && \
    apk add gcc libc-dev python3-dev && \
    pip3 install wheel && \
    pip3 wheel --wheel-dir=/srv/wheels /srv/src Faker


FROM alpine
LABEL maintainer="Alexander Zelenyak <zzz.sochi@gmail.com>"

EXPOSE 80/tcp 25/tcp

ENTRYPOINT ["python3", "-m", "smtp_faker"]
CMD ["--http=0.0.0.0:80", "--smtp=0.0.0.0:25"]

COPY --from=0 /srv/wheels /srv/wheels

RUN apk update && \
    apk add python3 &&\
    pip3 install wheel && \
    pip3 install Faker && \
    pip3 install --no-index --find-links=/srv/wheels smtp_faker && \
    rm -rf /srv/wheels

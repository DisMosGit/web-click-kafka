FROM python:3.9.5-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ARG CUSTOM_REQUIREMENTS
ARG CUSTOM_REQUIREMENTS=${CUSTOM_REQUIREMENTS:-requirements.txt}

COPY requirements.txt ./
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
COPY . ./

ARG ENV_FILE
ENV ENV_FILE=${ENV_FILE:-.env.dev}

EXPOSE 8080
# HEALTHCHECK --interval=1s --timeout=10s --start-period=1s --retries=3 CMD curl --fail http://localhost:8080/health-check || exit 1 # apt-get install curl

ENTRYPOINT [ "python" ]
CMD ["manage.py"]
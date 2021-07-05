import logging
import time
from pickle import dumps
from random import choice
from urllib.parse import urlencode

from kafka import KafkaProducer
from app.events.models import ClickManager
from app.auth.middlewares import users


logger = logging.getLogger()


def user():
    return choice(users)


def send_kafka_messages():
    producer = KafkaProducer(bootstrap_servers="kafka:9092")
    logger.info("start producer")
    while True:
        count = int(input("Enter count: "))
        if count <= 0:
            logger.info("stop producer")
            break
        for i in range(count):
            time.sleep(0.2)
            logger.info(f"{i}")
            try:
                producer.send(
                    "click-events",
                    dumps(ClickManager.IN.generate().dict() | {"user_id": user()}),
                    # urlencode(ClickManager.IN.generate().dict() | {"user_id": user()}).encode("utf-8"),
                )
            except Exception as e:
                logger.error(e)
                break

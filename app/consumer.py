import asyncio
import logging
from pickle import loads

from kafka import TopicPartition, KafkaConsumer

from app.events.models import Click

logger = logging.getLogger()


def get_kafka_messages():
    consumer = KafkaConsumer("click-events", bootstrap_servers="kafka:9092")
    logger.info("start consumer")
    for message in consumer:
        try:
            logger.info(
                "%s:%d:%d: key=%s value=%s"
                % (message.topic, message.partition, message.offset, message.key, message.value)
            )
            data = loads(message.value)
            asyncio.get_event_loop().run_until_complete(Click.add(Click.IN(**data), data.get("user_id")))
        except Exception as e:
            logger.error(e)

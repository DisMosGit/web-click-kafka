from typing import Optional
from uuid import UUID
from datetime import datetime
import orjson, pydantic
from pydantic.main import BaseModel

from app.db import ClickhouseTable, M


class ClickManager:
    class ClickIn(pydantic.BaseModel):
        x: pydantic.PositiveInt
        y: pydantic.PositiveInt
        window_x: pydantic.PositiveInt
        window_y: pydantic.PositiveInt
        duration: Optional[pydantic.PositiveInt]
        page: str

        @classmethod
        def generate(cls):
            from random import choice, randint

            pages = ("main", "index", "profile", "shop")
            return cls(
                x=randint(1, 12000),
                y=randint(1, 12000),
                window_x=randint(1, 12000),
                window_y=randint(1, 12000),
                duration=randint(1, 10000),
                page=choice(pages),
            )

    class ClickOut(pydantic.BaseModel):
        time: datetime
        x: pydantic.PositiveInt
        y: pydantic.PositiveInt
        window_x: pydantic.PositiveInt
        window_y: pydantic.PositiveInt
        duration: Optional[pydantic.PositiveInt]
        page: str
        user_id: Optional[UUID]

    IN = ClickIn
    OUT = ClickOut


class ClickTable(ClickhouseTable):
    db = "events"
    table = "click"

    @classmethod
    @property
    def sql_table(cls):
        return f"{cls.db}.{cls.table}"

    @classmethod
    async def init_table(cls):
        conn = await cls.conn
        async with conn.cursor(cursor=cls.cursor) as cursor:
            await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.db}")
            await cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {cls.db}.{cls.table}
                (
                    time     \t DateTime('UTC'),
                    x        \t UInt16,
                    y        \t UInt16,
                    window_x \t UInt16,
                    window_y \t UInt16,
                    duration \t UInt32,
                    page     \t String,
                    user_id  \t UUID NULL
                ) ENGINE = MergeTree
                    ORDER BY time
                """.replace(
                    "  ", ""
                ).replace(
                    "\t", " "
                )
            )

    @classmethod
    async def add(cls, obj: BaseModel, user_id: UUID = None, defaults={"time": "now()"}):
        query = f"""
        INSERT INTO {cls.sql_table} (time, x, y, window_x, window_y, duration, page, user_id) VALUES
        ({defaults["time"]}, {obj.x}, {obj.y}, {obj.window_x}, {obj.window_y}, {obj.duration}, '{obj.page}', '{user_id if user_id else "NULL"}');
        """
        return await cls.raw_execute(query)

    # @classmethod
    # async def add(cls, obj: BaseModel, user_id: UUID = None, defaults={"time": "now()"}):
    #     template = """
    #     INSERT INTO {{sql_table}} (time, x, y, window_x, window_y, duration, page, user_id) VALUES
    #     ({{time}}, {{x}}, {{y}}, {{window_x}}, {{window_y}}, {{duration}}, {{page}}, {{user_id}});
    #     """
    #     return await cls.execute(template, M(defaults, obj, user_id=user_id, sql_table=cls.sql_table))

    @classmethod
    async def select(cls, find: dict, defaults={}):
        template = f"SELECT t.* {cls.db}.{cls.table} t;"
        return await cls.execute(template, defaults | {"find": find})


class Click(ClickTable, ClickManager):
    pass


class Word(pydantic.BaseModel):
    value: str
    duration: Optional[pydantic.PositiveInt]
    page: str
    user_id: Optional[UUID]


class Following(pydantic.BaseModel):
    from_page: str
    to_page: str
    delay: pydantic.PositiveInt
    user_id: Optional[UUID]

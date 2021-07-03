import logging

from asynch import connect, connection
from asynch.cursors import DictCursor
from jinjasql import JinjaSql


class ClickhouseTable:
    j = JinjaSql(param_style="named")
    cursor = DictCursor
    db: str
    table: str
    table_scheme: str

    @classmethod
    @property
    def sql(cls, template: str, data: dict) -> tuple:
        return cls.j.prepare_query(template, data)

    @classmethod
    @property
    async def db(cls) -> connection.Connection:
        return await connect(
            host="127.0.0.1",
            port=9000,
            database="default",
            user="default",
            password="",
        )

    @classmethod
    async def raw_execute(cls, query: str, args=None):
        async with cls.db.cursor(cursor=cls.cursor) as cursor:
            return await cursor.execute(query=query, args=args)

    @classmethod
    async def execute(cls, template: str, data: dict = {}):
        return await cls.raw_execute(*cls.sql(template, data))

    @classmethod
    async def init_table(cls):
        async with cls.db.cursor(cursor=cls.cursor) as cursor:
            await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.db};")

    @classmethod
    async def add(cls, values: list, defaults={}):
        template = f"INSERT INTO {cls.db}.{cls.table} (*) VALUES;"
        return await cls.execute(template, defaults | {"values": values})

    @classmethod
    async def select(cls, find: dict, defaults={}):
        template = f"SELECT t.* {cls.db}.{cls.table} t;"
        return await cls.execute(template, defaults | {"find": find})

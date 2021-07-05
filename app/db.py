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
    def sql(cls, template: str, data) -> tuple:
        return cls.j.prepare_query(template, data=data)

    @classmethod
    @property
    async def conn(cls) -> connection.Connection:
        return await connect(
            host="127.0.0.1",
            port=9000,
            database="default",
            user="default",
            password="",
        )

    @classmethod
    async def raw_execute(cls, query: str, args=None):
        conn = await cls.conn
        async with conn.cursor(cursor=cls.cursor) as cursor:
            return await cursor.execute(query=query.replace("  ", ""), args=args)

    @classmethod
    async def execute(cls, template: str, data: dict = {}):
        return await cls.raw_execute(*cls.sql(template, data))

    @classmethod
    async def init_table(cls):
        conn = await cls.conn
        async with conn.cursor(cursor=cls.cursor) as cursor:
            await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.db};")

    @classmethod
    async def add(cls, defaults={}, **kwargs):
        template = f"INSERT INTO {cls.db}.{cls.table} (*) VALUES;"
        return await cls.execute(template, **kwargs, defaults=defaults)

    @classmethod
    async def select(cls, defaults={}, **kwargs):
        template = f"SELECT t.* {cls.db}.{cls.table} t;"
        return await cls.execute(template, **kwargs, defaults=defaults)


def M(*args, **kwargs) -> dict:
    """Join objects to dict"""
    result = {}
    for arg in args:
        if isinstance(arg, dict):
            result.update(arg)
        if hasattr(arg, "__dict__"):
            result.update(dict(arg))
    return result | kwargs

import asyncio
import os
from decouple import config
from aiobotocore.session import get_session

from api import TgClient as TgClientWithFile
from dcs import SendMessageResponse, GetUpdatesResponse, Message
from s3 import S3Client

async def cli():
    result_path = []

    async with TgClientWithFile(config('TELEGRAM_TOKEN')) as tg_cli:
        res = await tg_cli.get_updates()
        for x in res['result']:
            try:
                r = Message.Schema().load(x['message'])
                for k in r.photo:
                    res_path = await tg_cli.get_file(k['file_id'])
                    result_path.append(res_path)

            except TypeError:
                res_path = await tg_cli.get_file(r.document['file_id'])
                result_path.append(res_path)

        return result_path

async def run_uploader():
    # todo чтение из файла который был записан в cli() либо чтение из очереди
    cr = dict(
        endpoint_url=config('DSN_MINIO'),
        aws_secret_access_key=config('MINIO_ACCESS_KEY'),
        aws_access_key_id=config('MINIO_SECRET_KEY')
    )
    s3cli = S3Client(**cr)
    await s3cli.fetch_and_upload('tests', f'{res_path.file_path[7:]}',
                                 f'{tg_cli.API_FILE_PATH}{tg_cli.token}/{res_path.file_path}')



async def worker():
    cr = dict(
        endpoint_url=config('DSN_MINIO'),
        aws_secret_access_key=config('MINIO_ACCESS_KEY'),
        aws_access_key_id=config('MINIO_SECRET_KEY')
    )
    s3cli = S3Client(**cr)
    await s3cli.cr_bucket("tests")
    while True:
        await run_uploader()


if __name__ == '__main__':
    asyncio.run(worker())

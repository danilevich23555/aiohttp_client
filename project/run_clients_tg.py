import asyncio
import os

from api import TgClient as TgClientWithFile
from dcs import SendMessageResponse, GetUpdatesResponse, Message


async def cli():
    async with TgClientWithFile('') as tg_cli:
        res = await tg_cli.get_updates()
        # [print(x['message']['date'], x['message']['document']['file_name'],
        #           x['message']['document']['mime_type']) for x in res['result']]
        for x in res['result']:
            try:
                r = Message.Schema().load(x['message'])
                print(r.photo, r.date)
                print(r.document, r.date)
            except KeyError:
                pass
#
#
#
#
# async def worker():
#     while True:
#         await asyncio.sleep(2)
#         await cli()



# async def cli():
#     async with TgClientWithFile('') as tg_cli:
#         res = await tg_cli.get_file('')
#         # [print(x['message']['date'], x['message']['document']['file_name'],
#         #           x['message']['document']['mime_type']) for x in res['result']]
#         r=res
#         print(r.file_path)
#         res1 = await tg_cli.download_file('photos/file_1.jpg','/Users/danila/KTS/AIOHTTP_Client/file_1.jpg')


# async def s3():
#     cr = dict(
#         endpoint_url=os.getenv("MINIO_SERVER_URL"),
#         aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
#         aws_access_key_id=os.getenv("MINIO_ROOT_USER")
#     )
#     s3cli = S3Client(**cr)
#     await s3cli.stream_upload(
#         'test_bucket',
#         'bbabae8bcbce1.mov',
#         'https://lms-metaclass-prod.hb.bizmrg.com/media/019c3374-9099-4c49-9037-bbabae8bcbce.mov'
#     )


if __name__ == '__main__':
        asyncio.run(cli())
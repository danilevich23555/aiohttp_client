import io
import asyncio

from s3 import S3Client

async def s3_test():
    cr = dict(
        endpoint_url='',
        aws_secret_access_key='',
        aws_access_key_id=''
    )
    bucket = 'tests'
    filename = 'test.txt'
    folder = 'testoftest'
    key = '{}/{}'.format(folder, filename)
    print(key)
    s3cli = S3Client(**cr)
    print(s3cli.key_id)
    await s3cli.fetch_and_upload('tests', 'dog.gif', 'https://random.dog/d239ed62-ea35-4e89-8931-5b0c732bd2ae.gif')


if __name__ == '__main__':
    asyncio.run(s3_test())
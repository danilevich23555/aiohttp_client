import aiohttp
from marshmallow.exceptions import ValidationError

from api import TgClient, TgClientError
from base import Client
from dcs import GetFileResponse, File, Message, SendMessageResponse


class TgClientWithFile(TgClient):


    async def get_file(self, file_id: str) -> File:
        url = f'{self.get_base_path()}{self.token}' + '/getFile'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={'file_id': file_id}) as resp:
                res = await self._handle_response(resp)
                try:
                    gf_response: GetFileResponse = GetFileResponse.Schema().load(res)
                except ValidationError:
                    raise TgClientError
                return gf_response.result

    async def download_file(self, file_path: str, destination_path: str):
        url = f'{self.API_FILE_PATH}{self.token}/{file_path}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(resp.status)
                # if resp.status != 200:
                #     raise TgClientError
                with open(destination_path, 'wb') as fd:
                    async for data in resp.content.iter_chunked(1024):
                        print(data)
                        fd.write(data)

    async def send_document(self, chat_id, document_path):
        url = f'{self.get_base_path()}{self.token}' + '/sendDocument'
        async with aiohttp.ClientSession() as session:
            with open(document_path, 'rb') as fd:
                form_data = aiohttp.FormData()
                form_data.add_field('document', fd)
                form_data.add_field('chat_id', str(chat_id))
                async with session.post(url, data=form_data) as resp:
                    print(resp.status)
                    res_dict = await self._handle_response(resp)
                    try:
                        sm_response: SendMessageResponse = SendMessageResponse.Schema().load(res_dict)
                    except ValidationError:
                        raise TgClientError
                    return sm_response.result

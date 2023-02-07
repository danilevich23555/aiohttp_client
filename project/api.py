from typing import Optional, List, Any

import aiohttp
from marshmallow.exceptions import ValidationError
from base import ClientError, Client
from dcs import UpdateObj, Message, SendMessageResponse, File, GetFileResponse


class TgClientError(ClientError):
    pass


class TgClient(Client):  #todo Можно вынести все
    BASE_PATH = 'https://api.telegram.org/bot' #todo вынести в .env идет повторение в Client
    API_FILE_PATH = 'https://api.telegram.org/file/bot' #todo вынести в .env идет повторение в Client

    def __init__(self, token: str = ''):
        self.token = token
        super().__init__()

    async def _handle_response(self, resp) -> Any:
        return await resp.json()

    def get_path(self, url):
        return f'{self.get_base_path()}{self.token}/{url}'

    async def get_me(self) -> dict:
        return await self._perform_request('get', self.get_path('getMe'))

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        return await self._perform_request('get', self.get_path('getUpdates'))

    async def get_updates_in_objects(self, *args, **kwargs) -> List[UpdateObj]:
        raise NotImplementedError

    async def send_message(self, chat_id: int, text: str):
        params = {'chat_id':chat_id, 'text':text}
        resp = await self._perform_request('post', self.get_path(f'sendMessage'), json=params)
        print(resp)
        try:
            sm_response = SendMessageResponse.Schema().load(resp)
        except ValidationError:
                    raise TgClientError
        return sm_response.result


    async def get_file(self, file_id: str) -> File:
        url = f'{self.get_base_path()}{self.token}' + '/getFile'
        async with aiohttp.ClientSession() as session:                 #todo поменял на один контекстный менеджер aiohttp.ClientSession сам по себе контекстный менеджер
            response = await session.get(url, params={'file_id': file_id})
            res = await self._handle_response(response)
            try:
                gf_response: GetFileResponse = GetFileResponse.Schema().load(res)
            except ValidationError:
                raise TgClientError
            return gf_response.result

    async def download_file(self, file_path: str, destination_path: str):
        url = f'{self.API_FILE_PATH}{self.token}/{file_path}'
        async with aiohttp.ClientSession() as session: #todo заменить как на 14 и 15 строчке
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
        async with aiohttp.ClientSession() as session: #todo заменить как на 14 и 15 строчке
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
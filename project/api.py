from typing import Optional, List
from marshmallow.exceptions import ValidationError
from base import ClientError, Client
from dcs import UpdateObj, Message, SendMessageResponse


class TgClientError(ClientError):
    pass


class TgClient(Client):
    BASE_PATH = 'https://api.telegram.org/bot'
    API_FILE_PATH = 'https://api.telegram.org/file/bot'

    def __init__(self, token: str = ''):
        self.token = token
        super().__init__()

    async def _handle_response(self, resp):
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
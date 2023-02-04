from dataclasses import field
from typing import ClassVar, Type, List, Optional

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class MessageFrom:
    id: int
    first_name: str
    last_name: Optional[str]
    username: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    type: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class PrivateChat(Chat):
    id: int
    first_name: str
    last_name: str
    username: str


@dataclass
class GroupChat(Chat):
    id: int
    type: str
    title: str

@dataclass
class Document:
    file_name: str
    file_id: str

@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={'data_key': 'from'})
    chat: Chat
    date: int
    text: Optional[str]
    document: Optional[dict]
    photo: Optional[list]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class File:
    file_id: str
    file_unique_id: str
    file_size: int
    file_path: str


@dataclass
class GetFileResponse:
    ok: bool
    result: File

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

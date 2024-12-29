from dataclasses import dataclass

from motor.core import AgnosticClient

from infra.repositories.messages.base import BaseChatRepository


@dataclass
class MongoDBChatRepository(BaseChatRepository):
    ...

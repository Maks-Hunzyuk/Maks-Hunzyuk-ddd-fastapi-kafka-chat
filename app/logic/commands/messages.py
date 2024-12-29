from dataclasses import dataclass

from domain.entities.messages import Chat
from domain.values.massages import Title
from infra.repositories.messages.base import BaseChatRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsRepositoryException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(title=command.title):
            raise ChatWithThatTitleAlreadyExistsRepositoryException(command.title)
        title = Title(value=command.title)
        #TODO считать ивенты
        new_chat = Chat.create_chat(title=title)
        await self.chat_repository.add_chat(new_chat)
        return new_chat
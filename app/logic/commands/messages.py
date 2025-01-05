from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.values.massages import Text, Title
from infra.repositories.messages.base import BaseChatRepository, BaseMessagesRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.messages import ChatNotFoundException, ChatWithThatTitleAlreadyExistsRepositoryException


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
    

@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Chat]):
    message_repository: BaseMessagesRepository
    chats_repository: BaseChatRepository


    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)
        message = Message(text=Text(value=command.text))
        chat.add_message(message)
        await self.message_repository.add_message(chat_oid=command.chat_oid, message=message)
        
        return message
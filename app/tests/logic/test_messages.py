from faker import Faker

import pytest

from domain.entities.messages import Chat
from domain.values.massages import Title
from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.memory import MemoryChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsRepositoryException
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success():
    chat_repository_instance = MemoryChatRepository()
    mediator = Mediator()
    faker = Faker()
    chat_handler = CreateChatCommandHandler(chat_repository=chat_repository_instance)
    mediator.register_command(CreateChatCommand, [chat_handler])
    chat: Chat
    chat, *_ = (await mediator.handle_commands(CreateChatCommand(title=faker.text())))
    assert await chat_repository_instance.check_chat_exists_by_title(title=chat.title.as_generic_type())


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker
):
    title_text = faker.text()
    chat = Chat(title=Title(title_text))
    await chat_repository.add_chat(chat)

    with pytest.raises(ChatWithThatTitleAlreadyExistsRepositoryException):
        await mediator.handle_commands(CreateChatCommand(title=title_text))
    
    assert len(chat_repository._saved_chats) == 1
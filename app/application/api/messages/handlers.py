from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from punq import Container

from application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema, CreateMessageResponseSchema, CreateMessageSchema
from application.api.schemas import ErrorSchema
from domain.exeptions.base import ApplicationExeption
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import init_container
from logic.mediator import Mediator



router = APIRouter(
    tags=["Chat"]
)


@router.post(
    "/", 
    response_model=CreateChatResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Эндпоинт создает, новый чат если с таким назвонием уже существует, то возвращается 400 ошибка",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
    }
)
async def create_chat_handler(schema: CreateChatRequestSchema,
                              container: Container = Depends(init_container)) -> CreateChatResponseSchema:
    """Создать новый чат"""
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_commands(CreateChatCommand(title=schema.title))
    except ApplicationExeption as exeption:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exeption.message})
    
    return CreateChatResponseSchema.from_entity(chat)


@router.post(
        "/{chat_oid}/messages",
        status_code=status.HTTP_201_CREATED,
        description="Ручка на добавление нового сообщения в чат с переданным ObjectID",
        responses={
            status.HTTP_201_CREATED: {"model": CreateMessageSchema},
            status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
        }
)
async def create_massage_handler(
        chat_oid: str,
        schema: CreateMessageSchema,
        container: Container = Depends(init_container)
) -> CreateMessageResponseSchema:
    """ Добавить новое сообщение в чат """
    mediator: Mediator = container.resolve(Mediator)
    try:
        message, *_ = await mediator.handle_commands(CreateMessageCommand(text=schema.text, chat_oid=chat_oid))
    except ApplicationExeption as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})
    return CreateMessageResponseSchema.from_entity(message)

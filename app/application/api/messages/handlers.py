from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from application.api.schemas import ErrorSchema
from domain.exeptions.base import ApplicationExeption
from logic.commands.messages import CreateChatCommand
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
async def create_chat_handler(schema: CreateChatRequestSchema, container=Depends(init_container)):
    """Создать новый чат"""
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_commands(CreateChatCommand(title=schema.title))
    except ApplicationExeption as exeption:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exeption.message})
    
    return CreateChatResponseSchema.from_entity(chat)
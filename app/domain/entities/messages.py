from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.entities.base import BaseEntity
from domain.events.messages import NewMessageReceivedEvent
from domain.values.massages import Text, Title


@dataclass(eq=False)
class Message(BaseEntity):

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )

    text: Text

    
@dataclass(eq=False)
class Chat(BaseEntity):

    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
     
    title: Title
    
    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(NewMessageReceivedEvent(
            message_text=message.text.as_generic_type(),
            chat_oid=self.oid,
            message_oid=message.oid
            ))
    

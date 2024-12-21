from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.values.massages import Text, Title


@dataclass
class Message:

    oid: str = field(
        default_factory=lambda: str(uuid4),
        kw_only=True
    )

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )

    text: Text

    def __hash__(self):
        return hash(self.oid)
    
    def __eq__(self, __value: 'Message'):
        return self.oid == __value.oid

    


@dataclass
class Chat:

   
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )
    oid: str = field(
        default_factory=lambda: str(uuid4),
        kw_only=True
    )

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
     
    title: Title

    def __hash__(self):
        return hash(self.oid)
    
    def __eq__(self, __value: 'Chat'):
        return self.oid == __value.oid
    
    def add_message(self, message: Message):
        self.messages.add(message)
    

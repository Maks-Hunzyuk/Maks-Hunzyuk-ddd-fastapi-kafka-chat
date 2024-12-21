from dataclasses import dataclass

from domain.exeptions.messages import TitleTooLongExeption, EmptyTextExeption
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextExeption()
        
    def as_generic_type(self):
        return str(self.value)
    

@dataclass(frozen=True)
class Title(BaseValueObject):

    def validate(self):
        if not self.value:
            raise EmptyTextExeption()
        if len(self.value) > 255:
            raise TitleTooLongExeption(self.value)
    
    def as_generic_type(self):
        return str(self.value)

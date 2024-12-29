from dataclasses import dataclass

from domain.exeptions.base import ApplicationExeption

dataclass(eq=False)
class TitleTooLongExeption(ApplicationExeption):
    
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    @property
    def message(self):
        return f"Слишком длинный текст сообщения '{self.text[:255]}...'"
    

@dataclass(eq=False)
class EmptyTextExeption(ApplicationExeption):

    @property
    def message(self):
        return f"Текст не может быть пустым"
from dataclasses import dataclass

from domain.exeptions.base import ApplicationExeption

dataclass(eq=False)
class TitleTooLongExeption(ApplicationExeption):
    text: str

    @property
    def message(self):
        return f"Слишком длинный текст сообщения '{self.text[:255]}...'"
    

@dataclass(eq=False)
class EmptyTextExeption(ApplicationExeption):

    @property
    def message(self):
        return f"Текст не может быть пустым"
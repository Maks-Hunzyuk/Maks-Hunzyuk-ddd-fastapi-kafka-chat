from dataclasses import dataclass

from domain.exeptions.base import ApplicationExeption


@dataclass(eq=False)
class LogicException(ApplicationExeption):
    @property
    def message(self):
        return "В обработке запроса возникла ошибка"
    

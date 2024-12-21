from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationExeption(Exception):
    @property
    def message(self):
        return "Произошла ошибка приложения."
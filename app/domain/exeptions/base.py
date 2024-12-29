from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationExeption(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

    @property
    def message(self):
        return "Произошла ошибка приложения."
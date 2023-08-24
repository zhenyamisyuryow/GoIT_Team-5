from abc import ABC, abstractmethod

class ConsoleMessage(ABC):
    @abstractmethod
    def output(self, message: str):
        pass

class TerminalMessage(ConsoleMessage):
    def output(self, message: str) -> str:
        print(message)

class CommandsHandler:
    def __init__(self, command_res:ConsoleMessage):
        self.__processor = command_res

    def send_message(self, message):
        self.__processor.output(message)

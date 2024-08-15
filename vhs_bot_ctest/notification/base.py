from abc import ABC, abstractmethod


class BaseNotification(ABC):
    @abstractmethod
    def send(self, message) -> bool:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

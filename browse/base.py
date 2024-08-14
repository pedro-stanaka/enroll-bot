from abc import abstractmethod, ABC


class BaseSiteBrowser(ABC):
    def __init__(self, site, agent=None):
        self.site = site
        self.agent = agent

    @abstractmethod
    def is_place_available(self):
        pass

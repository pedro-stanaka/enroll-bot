from vhs_bot_ctest.browse.base import BaseSiteBrowser
from vhs_bot_ctest.browse.vhs_berlin import VhsBerlinBrowser


class Registry:
    browsers: dict[str, BaseSiteBrowser]

    def __init__(self):
        self.browsers = {}

    def register_browser(self, browser: BaseSiteBrowser):
        self.browsers[browser.name()] = browser

    def get_browser(self, name: str):
        return self.browsers[name]

    def get_all(self) -> list[BaseSiteBrowser]:
        return self.browsers.values()

    def get_names(self) -> list[str]:
        return self.browsers.keys()


BrowserRegistry = Registry()
BrowserRegistry.register_browser(VhsBerlinBrowser())

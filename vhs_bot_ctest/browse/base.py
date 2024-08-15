from abc import ABC, abstractmethod

from playwright.sync_api import sync_playwright


class BaseSiteBrowser(ABC):
    def __init__(self, site):
        self.site = site

    def get_text_for_element(self, element, agent=None):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            if agent:
                context = browser.new_context(user_agent=agent)
            page = context.new_page()
            page.goto(self.site)
            return page.query_selector(element).inner_text()

    @staticmethod
    @abstractmethod
    def name():
        pass

    @abstractmethod
    def human_name(self):
        pass

    @abstractmethod
    def is_place_available(self, agent=None):
        pass

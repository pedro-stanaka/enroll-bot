from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright, Error as PlaywrightError
import time
import structlog

class ElementNotFoundError(ValueError):
    pass

class NetworkError(ValueError):
    pass

class BaseSiteBrowser(ABC):
    def __init__(self, site):
        self.site = site
        self.logger = structlog.get_logger()
        self.max_retries = 3
        self.retry_delay = 5  # seconds

    def get_text_for_element(self, element, agent=None):
        for attempt in range(self.max_retries):
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context()
                    if agent:
                        context = browser.new_context(user_agent=agent)
                    page = context.new_page()
                    page.goto(self.site)
                    wanted_el = page.query_selector(element)
                    if wanted_el:
                        text = wanted_el.inner_text()
                        browser.close()
                        return text
                    browser.close()
                    raise ElementNotFoundError(f"Element {element} not found on the page {self.site}")
            except PlaywrightError as e:
                browser.close()
                if attempt < self.max_retries - 1:
                    self.logger.warn(
                        "Network error occurred, retrying...",
                        error=str(e),
                        attempt=attempt + 1,
                        max_retries=self.max_retries
                    )
                    time.sleep(self.retry_delay)
                else:
                    raise NetworkError(f"Failed to access {self.site} after {self.max_retries} attempts: {str(e)}")

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

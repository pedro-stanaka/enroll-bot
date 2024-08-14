from browse.base import BaseSiteBrowser
from playwright.sync_api import sync_playwright


class VhsBerlinBrowser(BaseSiteBrowser):
    def is_place_available(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(self.site)
            message = page.query_selector("#bomain #error_message").inner_text()

            if "wurden keine Kurse gefunden" in message:
                return False

        return True

from vhs_bot_ctest.browse.base import BaseSiteBrowser, ElementNotFoundError
import structlog
from playwright.sync_api import sync_playwright
import time
from datetime import datetime

class BerlinPassportBrowser(BaseSiteBrowser):
    def __init__(self):
        super().__init__("https://service.berlin.de/terminvereinbarung/termin/all/121151/")
        self.logger = structlog.get_logger()

    @staticmethod
    def name():
        return "berlin_passport"

    def human_name(self):
        return "Berlin Passport Appointment"

    def is_place_available(self, agent=None):
        """
        Checks if there are any available appointments for passport services in Berlin.
        Returns True if appointments are available in the current month, False otherwise.
        """
        try:
            # First check if the "no appointments" message is shown
            no_appointments_text = self.get_text_for_element(".herounit-article--default .title", agent)
            if "keine termine" in no_appointments_text.lower():
                self.logger.warn(
                    "No appointments available",
                    message="The page explicitly states that no appointments are available at this time",
                    details="The system shows the 'no appointments' message and no calendar is displayed"
                )
                return False

            # Get current month in German
            german_months = {
                1: "Januar",
                2: "Februar",
                3: "März",
                4: "April",
                5: "Mai",
                6: "Juni",
                7: "Juli",
                8: "August",
                9: "September",
                10: "Oktober",
                11: "November",
                12: "Dezember"
            }
            current_month = german_months[datetime.now().month]

            # Check for any elements with class "buchbar" which indicates available appointments
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                if agent:
                    context = browser.new_context(user_agent=agent)
                page = context.new_page()
                page.goto(self.site)

                # Get all calendar month tables
                month_tables = page.query_selector_all(".calendar-month-table")

                # Track the next available month shown
                next_month = None
                for table in month_tables:
                    month_header = table.query_selector(".month")
                    if month_header:
                        month_text = month_header.inner_text()
                        if not next_month:  # Store the first month we see
                            next_month = month_text.split()[0]  # Get just the month name
                        if current_month in month_text:
                            available_dates = table.query_selector_all(".buchbar")
                            if available_dates:
                                self.logger.info(
                                    f"{current_month} appointments available",
                                    message=f"Found available appointment dates in {current_month}",
                                    count=len(available_dates)
                                )
                                browser.close()
                                return True

                browser.close()
                self.logger.warn(
                    "No appointments available",
                    message=f"Next available calendar shown is for {next_month}",
                    details=f"The calendar is displayed but no {next_month} dates are marked as available"
                )
                return False

        except ElementNotFoundError:
            # If we can't find either element, log it and return False
            self.logger.warn(
                "Could not determine appointment availability",
                message="Neither the calendar nor the 'no appointments' message could be found",
                details="This might indicate a change in the page structure or a temporary issue"
            )
            return False

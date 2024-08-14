from vhs_bot_ctest.browse.base import BaseSiteBrowser


class VhsBerlinBrowser(BaseSiteBrowser):
    COURSES_URL = "https://www.vhsit.berlin.de/vhskurse/BusinessPages/CourseSearch.aspx?direkt=1&begonnen=0&beendet=0&stichw=Pr%FCfungstermin%20Einb%FCrgerungstest"

    def __init__(self):
        super().__init__(self.COURSES_URL)

    @staticmethod
    def name():
        return "vhs_citizenship"

    def is_place_available(self, agent=None):
        message = self.get_text_for_element("#bomain #error_message", agent)
        return "wurden keine Kurse gefunden" not in message

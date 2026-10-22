
import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class HackForgeTests(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Remote(
            command_executor=os.getenv(
                "SELENIUM_URL",
                "http://localhost:4444/wd/hub"
            ),
            options=options
        )

    def tearDown(self):
        if hasattr(self, "driver"):
            self.driver.quit()

    def test_hackforge_website_loads(self):
        url = os.getenv(
            "APP_URL",
            "http://localhost:5001"
        )

        self.driver.get(url)
        WebDriverWait(self.driver, 15).until(
            lambda driver: driver.title != ""
        )

        self.assertIn("HackForge", self.driver.title)
        self.assertTrue(self.driver.find_elements("tag name", "body"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

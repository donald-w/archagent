#%% [markdown]
"""
# Selenium Web Scraping Examples
This file demonstrates how to use Selenium with Python to navigate web pages
and execute JavaScript queries.
"""

#%% Setup and Imports
# region: Initial Setup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
# endregion

#%% [markdown]
"""
## WebScraper Class
A class that handles web navigation and JavaScript execution
"""

#%% WebScraper Class Implementation
# region: WebScraper Class
class WebScraper:
    def __init__(self, headless=False):
        """Initialize the WebScraper with Chrome options"""
        # Set up Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 10)
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        self.driver.get(url)
        time.sleep(2)  # Wait for page to load
    
    def execute_js(self, js_code):
        """Execute JavaScript code and return the result"""
        return self.driver.execute_script(js_code)
    
    def get_element_text(self, selector, by=By.CSS_SELECTOR):
        """Get text content of an element using various selectors"""
        element = self.wait.until(
            EC.presence_of_element_located((by, selector))
        )
        return element.text
    
    def get_page_title(self):
        """Get the page title using JavaScript"""
        return self.execute_js("return document.title;")
    
    def get_all_links(self):
        """Get all links on the page using JavaScript"""
        return self.execute_js("""
            return Array.from(document.getElementsByTagName('a'))
                .map(a => ({text: a.text, href: a.href}));
        """)
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page using JavaScript"""
        self.execute_js("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Wait for any dynamic content to load
    
    def close(self):
        """Close the browser"""
        self.driver.quit()
# endregion

#%% [markdown]
"""
## Example Usage
Demonstrating how to use the WebScraper class
"""

#%% Example Usage
# region: Example Usage
def main():
    # Initialize the scraper
    scraper = WebScraper(headless=False)
    
    try:
        # Navigate to a website
        scraper.navigate_to("https://www.python.org")
        
        # Get page title using JavaScript
        title = scraper.get_page_title()
        print(f"Page Title: {title}")
        
        # Get text from a specific element using CSS selector
        download_text = scraper.get_element_text("#downloads")
        print(f"Download section text: {download_text}")
        
        # Get all links on the page
        links = scraper.get_all_links()
        print("\nFirst 5 links on the page:")
        for link in links[:5]:
            print(f"Text: {link['text']}")
            print(f"URL: {link['href']}\n")
        
        # Scroll to bottom and get more content
        scraper.scroll_to_bottom()
        
        # Pause before closing
        input("\nPress Enter to run JavaScript query...")
        
        # Example: Get all headings from the page
        headings = scraper.execute_js("""
            return Array.from(document.querySelectorAll('h1, h2, h3'))
                .map(h => ({level: h.tagName, text: h.textContent.trim()}));
        """)
        
        print("\nPage Headings:")
        for heading in headings:
            print(f"{heading['level']}: {heading['text']}")
        
        input("\nPress Enter to close the browser...")
        
    finally:
        # Always close the browser
        scraper.close()

if __name__ == "__main__":
    main()
# endregion 
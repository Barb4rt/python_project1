import requests
from bs4 import BeautifulSoup as bs


class Page:
    @staticmethod
    def get_page_content(url):
        """
        static method to retrieve information from a page

        Args:
            url (string): Where retrieve the content

        Returns:
            class: Class of beautiful soup
        """
        try:
            return bs(requests.get(url).content, "html5lib")
        except Exception:
            print(Exception)

    @staticmethod
    def get_categories_list(uri, page):
        """
        static method to retrieve list of category of the page

        Args:
            uri (string): The domain address
            page (Class): The page to scrap

        Returns:
            List: List of categories
        """
        return [
            (
                li.find("a").string.strip().lower().replace(" ", "_"),
                f"{uri}/{li.find('a', href=True)['href']}",
            )
            for li in page.find("aside").find("ul").find("li").find_all("li")
        ]

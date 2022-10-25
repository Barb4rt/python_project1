from importlib.resources import path
from modules.page import Page
from modules.helper import Helper


class Category(Helper):
    """A class taht represente a Category inheritance of the class Helper"""

    def __init__(self, name, url):
        """
        Args:
            name (string): The name of category
            url (string): The url of the category
        """
        self.name = name
        self.url = url
        self.page = self._get_category_page()
        self.book_list = self._get_books_urls()
        self.number_of_books

    def _get_category_page(self):
        """
            private method to retrieve the page content

        Returns:
            string: the page content
        """
        return Page.get_page_content(self.url)

    def _get_category_pages_urls(self):
        """
        private method to retrieve all page urls related to the current category

        Returns:
            list: List of page's url
        """
        try:
            page_number = (
                int(self.page.find("li", class_="current").string.strip()[-1])
                if self.page.find("li", class_="current")
                else 1
            )
            if page_number > 1:
                urls = [
                    self.url.replace("index.html", f"page-{i+1}.html")
                    for i in range(page_number)
                ]
                return urls
            return [self.url]
        except Exception:
            print(Exception)

    def _get_books_urls(self):
        """
        private method to get all the url of the books of the current category

        Returns:
            List: List of book's url
        """
        try:
            uri = "http://books.toscrape.com"
            books_list = []
            for url in self._get_category_pages_urls():
                page = Page.get_page_content(url)
                title = page.find_all("h3")
                [
                    books_list.append(
                        f"{uri}/catalogue{link.find('a', href=True)['href'].split('.', 6)[-1]}"
                    )
                    for link in title
                ]
            self.number_of_books = len(books_list)
            return books_list
        except Exception:
            print(Exception)

    def create_categorie_dir(self, path):
        """
        Creation of files for the category instance

        Args:
            path (string): Where to create the directories
        """
        self.folder_path = self.create_directory(self.name, path)
        self.media_dir = self.create_directory("media", self.folder_path)

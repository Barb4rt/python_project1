"""Class represents a book
"""


class Book:
    @staticmethod
    def book_format(page, url):
        """Format the data from the page to the format desired in CSV file

        Args:
            page (string): The book page
            url (string): The url of the book

        Yields:
            iterable: an iterable of the book
        """
        MAP_INTEGER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        yield url
        yield page.find("tbody").find_all("tr")[0].find("td").string
        yield page.find("div", class_="product_main").find("h1").string
        yield page.find("tbody").find_all("tr")[3].find("td").string
        yield page.find("tbody").find_all("tr")[2].find("td").string
        yield page.find("tbody").find_all("tr")[5].find("td").string.split()[
            -2
        ].replace("(", "")
        yield page("div", id="product_description")[
            0
        ].next_sibling.next_sibling.string if page(
            "div", id="product_description"
        ) else "No description"
        note = (
            page.find("div", class_="product_main")
            .find("p", class_="star-rating")["class"][-1]
            .lower()
        )
        note = MAP_INTEGER[note]
        yield str(note) + "/5"
        yield "http://books.toscrape.com" + page.find("img")["src"].split(".", 4)[-1]

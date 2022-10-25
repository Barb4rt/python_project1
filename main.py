import os
import time
from alive_progress import alive_bar
from alive_progress.animations import bouncing_spinner_factory
from modules import *

start_time = time.time()
base_path=os.getcwd() + "\\" if "\\" in os.getcwd() else "/"
data_dir = Helper.create_directory('data',base_path)
uri = "http://books.toscrape.com"
spinner = bouncing_spinner_factory(
    "🖊️", 8, hide=False, background=".", overlay=False
)
headers = [
    "url",
    "upc",
    "titre",
    "prix avec taxe",
    "prix sans taxe",
    "disponible",
    "description",
    "categorie",
    "note",
    "chemin de l'image",
]
for categorie in Page.get_categories_list(uri=uri, page=Page.get_page_content(f"{uri}/index.html")):
    categorie = Category(*categorie)
    categorie.create_categorie_dir(data_dir)
    csv = Csv(categorie.name, categorie.folder_path, headers=headers)
    csv.create_csv_file()
    with alive_bar(len(categorie.book_list), spinner=spinner) as bar:
        for book_url in categorie.book_list:
            bar()
            book = list(Book.book_format(Page.get_page_content(book_url), book_url))
            ThreadHandler(2,"download",
                Download.download_image(book[2], book[-1], categorie.media_dir)
            ).start()
            bar.text = f"-> Write into CSV file {book[2]} data , please wait..."
            csv.append_into_csv(book)
            bar.text = f"-> End Process for {book[2]} Next ..."
print("--- %s seconds ---" % (time.time() - start_time))

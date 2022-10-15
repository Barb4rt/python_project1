import requests
from queue import Empty, Queue
import os
from bs4 import BeautifulSoup as bs
import re
import csv
import time
from download_image import DownloadImage
from alive_progress import alive_bar
from alive_progress.animations import bouncing_spinner_factory
from threading import Thread


def start_queue(queue):
    while True:
        try:
            queue.get()
        except Empty:
            continue
        else:
            queue.task_done()

def run_queue(queue):
    handler_thread = Thread(target=start_queue, args=(queue,), daemon=True)
    handler_thread.start()


def get_page_content(url):
    try:
        return bs(requests.get(url).content, 'html5lib')
    except Exception:
        print(Exception)


def get_categories_list(uri, page):
    return [(li.find('a').string.strip().lower().replace(" ", "_"), f"{uri}/{li.find('a', href=True)['href']}") for li in page.find('aside').find('ul').find('li').find_all('li')]


def book_generator(page, url):
    MAP_INTEGER = {"one": 1,
                   "two": 2,
                   "three": 3,
                   "four": 4,
                   "five": 5}
    yield url
    yield page.find('tbody').find_all('tr')[0].find('td').string
    yield page.find('div', class_='product_main').find('h1').string
    yield page.find('tbody').find_all('tr')[3].find('td').string
    yield page.find('tbody').find_all('tr')[2].find('td').string
    yield page.find('tbody').find_all('tr')[5].find('td').string.split()[-2].replace('(', "")
    yield page('div', id='product_description')[0].next_sibling.next_sibling.string if page('div', id='product_description') else "No description"
    note = page.find('div', class_='product_main').find(
        'p', class_='star-rating')['class'][-1].lower()
    note = MAP_INTEGER[note]
    yield str(note) + "/5"
    yield "http://books.toscrape.com" + page.find('img')['src'].split('.', 4)[-1]


def get_pages_number(page):
    return int(page.find('li', class_='current').string.strip()[-1]) if page.find('li', class_='current') else 1


def create_csv_file(path_dir, name):
    with open(f'{path_dir}/{name}.csv', "w", newline='', encoding='utf-8') as fi:
        writer = csv.writer(fi, delimiter=';')
        writer.writerow(["url", "upc", "titre", "prix avec taxe", "prix sans taxe",
                        "disponible", "description", "categorie", "note", "chemin de l'image"])
    return f'{path_dir}/{name}.csv'


def append_into_csv(data, path):
    with open(path, "a") as fi:
        writer = csv.writer(fi, delimiter=';')
        writer.writerow(
            [re.sub('[^A-Za-z0-9,\/.-_\'" -]', '', str(d))for d in data])
    fi.close


def create_directory(path, name):
    print(f'Création du dossier {name}...')
    separation = '\\' if "\\" in path else "/"
    fullpath = path + name
    print(fullpath)
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
        print(f'Le dossier {name} crée')
    else:
        print(f'Le dossier {name} existe déja')
    return fullpath + separation


def main():
    queue = Queue()
    work_queue = DownloadImage(queue)
    spinner = bouncing_spinner_factory(
        '🖊️', 8, hide=False, background=".", overlay=False)
    run_queue(work_queue.q)
    book_count = 0
    base_path = os.getcwd() + "\\" if "\\" in os.getcwd() else "/"
    data_path = create_directory(base_path, 'data')
    uri = "http://books.toscrape.com"
    soup = get_page_content(f"{uri}/index.html")
    categories_list = get_categories_list(uri, soup)
    for categorie in categories_list:
        name, url = categorie
        categories_path =  create_directory(data_path, name)
        media_path, csv_path = create_directory( categories_path, 'media'), create_csv_file(categories_path, name) 
        page =get_page_content(url)
        page_number, product_list =  get_pages_number(page), []
        if page_number > 1:
            urls = [url.replace('index.html', f'page-{i+1}.html') for i in range(page_number)]
            for url in urls:
                page = get_page_content(url)
                page = page.find_all('h3')
                [product_list.append(f"{uri}/catalogue{link.find('a', href=True)['href'].split('.', 6)[-1]}") for link in page]
                print(len(product_list))
        else:
            product_list = [uri + "/catalogue" + element.find(
                'a', href=True)['href'].split(".", 6)[-1] for element in page.find_all('h3')]
        with alive_bar(len(product_list), spinner=spinner) as bar:
            for product_url in product_list:
                bar()
                book_count += 1
                page = get_page_content(product_url)
                book = list(book_generator(page, product_url))
                work_queue.add_to_queue(book[2], book[-1], media_path)
                bar.text = f'-> Scrape page of book {book[2]}, please wait...'
                bar.text = f'-> Write into CSV file {book[2]} data , please wait...'
                append_into_csv(book, csv_path)
                bar.text = f'-> End Process for {book[2]} Next ...'
    queue.join
    print(book_count)

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))

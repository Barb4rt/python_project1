import requests
import os
from bs4 import BeautifulSoup as bs
import re
import csv
import time


class Category():
    def __init__(self,page,localisation):
        self.name = page.find('a').string.strip().lower()
        self.base_path= localisation
        self.path_dir = localisation + "\\" if "\\" in localisation else "/" + self.name if os.path.exists( f'{localisation}{self.name}') else None 
        self.media_path_dir = localisation + "\\" if "\\" in localisation else "/" + "media" if os.path.exists( f'{localisation}{self.name}/media') else None 
        self.url = f"http://books.toscrape.com/{page.find('a',href=True)['href']}"
        self.product_list= []
        self.page_number = 1

    def get_category_page(self):
        print(self.url)
        return get_page_content(self.url)
    
    def get_pages_number(self):
        page_content= self.get_category_page()
        self.page_number = int(page_content.find('li', class_='current').string.strip()[-1]) if page_content.find('li', class_='current') else 1

    def get_product_list(self):
        self.get_pages_number()
        print(self.page_number)
        if self.page_number > 1 :
             for i in range(self.page_number):
                soup = get_page_content(self.url.replace('index.html', f'page-{i+1}.html'))
                [self.product_list.append(Product(get_page_content("http://books.toscrape.com/catalogue" + product.find('a' , href=True)['href'].split(".",6)[-1]),url="http://books.toscrape.com/catalogue" + product.find('a' , href=True)['href'].split(".",6)[-1],category=self.name)) for product in soup.find_all('h3')]
        else:
            soup = get_page_content(self.url)
            [self.product_list.append(Product(get_page_content("http://books.toscrape.com/catalogue" + product.find('a' , href=True)['href'].split(".",6)[-1]),url="http://books.toscrape.com/catalogue" + product.find('a' , href=True)['href'].split(".",6)[-1],category=self.name)) for product in soup.find_all('h3')]
        return self.product_list

    def create_dir(self,path=None, name=None):
        if name != None:
            path = path if path else self.path_dir
            self.media_path_dir = create_directory(path,name)
            return
        self.path_dir = create_directory(self.path_dir,self.name)

    def create_csv_file(self):
        print(self.path_dir)
        with open(f'{self.path_dir}/{self.name}.csv',"w", newline='',encoding='utf-8') as fi:
            writer = csv.writer(fi, delimiter=';')
            writer.writerow(["url","upc","titre","prix avec taxe","prix sans taxe","disponible","description","categorie", "note" ,"chemin de l'image"])
    
    def get_path_dir(self):
        return self.path_dir + "\\" if "\\" in self.path_dir else "/" 
    def get_media_path_dir(self):
        return self.media_path_dir + "\\" if "\\" in self.path_dir else "/" 

class Product():
    def __init__(self, page, url, category):
        self.product_page_url = url
        self.upc = page.find('tbody').find_all('tr')[0].find('td').string
        self.title = page.find('div', class_='product_main').find('h1').string
        self.price_including_tax = page.find('tbody').find_all('tr')[3].find('td').string
        self.price_excluding_tax = page.find('tbody').find_all('tr')[2].find('td').string
        self.number_available = page.find('tbody').find_all('tr')[5].find('td').string.split()[-2].replace('(',"")
        self.product_description =  page('div', id='product_description')[0].next_sibling.next_sibling.string if page('div', id='product_description') else "No description"
        self.category = category
        self.review_rating = page.find('div', class_='product_main').find('p', class_='star-rating')['class'][-1]
        self.image_url = "http://books.toscrape.com"+ page.find('img')['src'].split('.',4)[-1]

    def append_into_csv(self,path):
        data = [self.product_page_url,self.upc,self.title,self.price_including_tax,self.price_excluding_tax,self.number_available,self.product_description,self.category,self.review_rating,self.image_url]
        with open(f'{path}/{self.category}.csv',"a") as fi:
            writer = csv.writer(fi, delimiter=';')
            writer.writerow([re.sub('[^A-Za-z0-9,\/.-_\'" -]', '', str(d))for d in data])
        fi.close

    def download_image(self, path):
        filename= re.sub('[^A-Za-z0-9]','', self.title)
        file_ext = self.image_url.split(".",-1)[-1]
        filename = filename +'.'+file_ext
        print(path)
        img_data = requests.get(self.image_url).content
        with open(path+filename, 'wb') as fi: 
            fi.write(img_data)
        
def get_page_content(url):
  return bs(requests.get(url).content, 'html5lib')

def create_directory(path,name):
    print(f'Création du dossier {name}...')
    if not os.path.exists(path+name):
        os.makedirs(path+name)
        print(f'Le dossier {name} crée')
    else:
        print(f'Le dossier {name} existe déja')
    print(path+name)
    return str(path+name)
      
def create_csv_file(header,data):
    with open('data.csv',"w") as fi:
        writer = csv.writer(fi, delimiter=',')
        writer.writerow(header)
        writer.writerow(data)
    fi.close


def main():
    # * Definir l'adresse URL du site où extraire les données
    url = "http://books.toscrape.com"
    # Recuperation du chemin du dossier courant
    base_path = os.getcwd() + "\\" if "\\" in os.getcwd() else "/"
    # * Creation du dossier pour le stockage des données
    data_path = create_directory(base_path,"data")
    # *Extraire la liste des categories
    soup = get_page_content(url+"/index.html")
    categories = soup.find('aside').find('ul').find('li').find_all('li')
    for category in categories:
        category_instance = Category(category,data_path)
        # * crée un dossier dans le dossier data/<nom de la catégorie>
        category_instance.create_dir()
        category_instance.create_csv_file()
        category_instance.create_dir(category_instance.get_path_dir() , "media")
        # * Récupération de la liste des produits
        category_instance.get_product_list()
        # *Créé un fichier csv pour chaque categorie
        # ? Pour chaque produit :
        for book in category_instance.product_list:
            # * récupérer le chemin du dossier crée pour chaque catégories
            # *Créé une ligne csv avec les information du produit
            book.download_image(category_instance.get_media_path_dir())
            book.append_into_csv(category_instance.path_dir) 
            # *Enregistrer l'image
start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
import requests as req
from bs4 import BeautifulSoup

def sort_name(name):
    #удаляет пробелы из названия продукта
    name_list = name.split()
    sorted_name = " ".join(name_list)
    return sorted_name


def create_soup_page(url):
    webpage = req.get(url)
    webpage_text = webpage.text
    soup = BeautifulSoup(webpage_text, "html.parser")
    return soup


def dns_scrape(url):
    #Возвращяет цену для днс
    soup = create_soup_page(url)
    try:
        price_units = soup.find("p", class_="pricePerUnit").getText().strip()
        product_price = price_units.partition("/")[0]
        if "p" in product_price:
            product_price_pence = product_price.replace("p", "")
            product_price_final = float(product_price_pence)/100
        else:
            product_price_final = price_units.partition("/")[0][1:]

        return product_price_final

    except AttributeError:
        print("Failed- investigate: {}".format(url))


def mvideo_scrape(url):
    #Возвращяет цену для мвидео
    soup = create_soup_page(url)
    try:
        product_description = soup.find("div", class_="related-search-ribbon-enabled")

        try:
            product_price_raw = product_description.find(class_="nowPrice").getText()
            product_price = product_price_raw.strip()[1:]
        except AttributeError:
            # Если текущая цена недоступна,это означает,что товар не выставлен на продажу.
            product_price_raw = product_description.find(class_="typicalPrice").getText()
            product_price = product_price_raw.strip()[1:]

        return product_price
    except AttributeError:
        print("Failed- investigate: {}".format(url))


def regard_scrape(url):
    #Возвращяет цену для регард
    soup = create_soup_page(url)
    try:
        product_price = soup.find(class_="value").getText()
        return product_price

    except AttributeError:
        print("Failed- investigate: {}".format(url))

from bs4 import BeautifulSoup
import requests
import csv
from PIL import Image


def start() -> csv:
    url = 'https://chudodey.com'
    headers = {'User-Agent': 'Mozilla/5.0'}

    with open(f"products.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Путь',
                'Название',
                'Описание',
                'Артикул',
                'Цена',
                'Старая цена',
                'Возможны вариации',
                'Фото'
            )
        )

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'html.parser')

    all_categories_hrefs = soup.find_all(class_='dropdown-item dropdown-item_header')
    all_categories_dict = {}
    for item in all_categories_hrefs:
        item_text = item.text
        item_href = item.get("href")
        all_categories_dict[item_text] = item_href

    count = 0
    for category_name, category_href in all_categories_dict.items():
        if count < 5:
            count += 1
            req = requests.get(category_href, headers=headers)
            soup2 = BeautifulSoup(req.text, 'html.parser')
            all_numbers_pages = soup2.find_all(class_="pagination-item")

            # for number_page in range(0, (int(all_numbers_pages[-2].text))):
            for number_page in range(0, 1):
                link_category = category_href + f'/filters/filter10/filter_type/SG/filters/filter10/filter_name/в%20наличии%20и%20под%20заказ/filters/filter10/values/sort/field_name/title/sort/sort_type/возрастание/pager/page_number/{number_page}'
                req = requests.get(link_category, headers=headers)
                soup3 = BeautifulSoup(req.text, 'html.parser')
                all_href_products = soup3.find_all(class_='product__brief')
                for item in all_href_products:
                    link_product = item.find("a").get("href")
                    req = requests.get(link_product, headers=headers)
                    soup4 = BeautifulSoup(req.text, 'html.parser')

                    breadcrumb = soup4.find(class_="breadcrumb").text
                    name = soup4.find(class_="product-detail__header").text
                    image = soup4.find(class_="product-detail__image").find("img")
                    image_url = image['data-src']
                    img = Image.open(requests.get(image_url, stream=True).raw)
                    img.save(f'data/{name}.jpg')
                    description = soup4.find(class_="row product-detail__properties").text
                    vendor_code = soup4.find(class_="invisible-line product-detail__articul").text
                    price = soup4.find(class_="product-detail__price").text
                    old_price = soup4.find(class_="old-price")
                    if old_price is not None:
                        old_price = old_price.text
                    try:
                        options = soup4.find(class_="product-group-change-in-cart invisible-line").find_all(
                            class_="colour-select colour-select-lg")
                        options_list = []
                        for option in options:
                            option = str(option).split('"')[3]
                            options_list.append(option)
                        if not options_list:
                            options = soup4.find(class_="product-detail__colours").find_all(class_="text-select")
                            for option in options:
                                option = str(option).split('"')[3]
                                options_list.append(option)
                    except:
                        options_list = None
                    with open("products.csv", "a", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                breadcrumb,
                                name,
                                description,
                                vendor_code,
                                price,
                                old_price,
                                options_list,
                                image_url
                            )
                        )


if __name__ == '__main__':
    start()

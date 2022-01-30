import requests
from bs4 import BeautifulSoup as BS
import pymysql.cursors
from pprint import pprint

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='store',
                             cursorclass=pymysql.cursors.DictCursor)

url = "https://jumia.com.ng/tablets/"
headers = requests.utils.default_headers()
headers.update({
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
})

categories = []
names = []
prices = []

for page in range(1,51):
    my_response = requests.get(f"https://www.jumia.com.ng/tablets/?page={page}#catalog-listing")

    first_soup = BS(my_response.content, features="lxml")
    second_soup = first_soup.find("div", {"class" : "-paxs row _no-g _4cl-3cm-shs"})
    each_card = second_soup.find_all("article", {"class" : "prd _fb col c-prd"})
    for card in each_card:
        # print(card.prettify)
        card_details = card.find("a")
        
        category = card_details.get("data-category")
        category = category.split("/")
        categories.append(category[-1])
        # print(categories)

        name = card_details.get("data-name")
        name = name.replace("'", "")
        names.append(name)
        # print(names)

        price = card.find("div", {"class": "prc"})
        price = (price.text).split(" - ")
        pri = price[-1]
        price = int((pri).lstrip("₦ ").replace(",", ""))
        
        prices.append(price)
        # print(price)

        merged_list = list(zip(names,categories, prices))

def insert():
    with connection:
        with connection.cursor() as cursor:
            for desc,type, value in merged_list:
                sql = "INSERT INTO product(Name, Category, Price) VALUES('{}', '{}', '{}')".format(desc, type, value)
                cursor.execute(sql)
        connection.commit()
# insert()

user_input = input("=>:\n")
with connection:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM product WHERE Name LIKE '%{}%' ORDER BY ID ASC".format(user_input)
        cursor.execute(sql)
        result = cursor.fetchall()
        pprint(result)





from bs4 import BeautifulSoup
import requests
import time

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'price/index.html')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

flipkart = ''
amazon = ''


def next(request):
    name = request.GET.get("text", "default")
    name1 = name.replace(" ", "-")
    name2 = name.replace(" ", "+")
    flipkart = request.GET.get('flipkart', 'on')
    amazon = request.GET.get('amazon', 'on')

    infor = []
    rate = []

    if amazon == "on":
        try:
            amazon = f'https://www.amazon.in/{name1}/s?k={name2}'
            res = requests.get(
                f'https://www.amazon.in/{name1}/s?k={name2}', headers=headers)
            print("\nSearching in amazon:")
            soup = BeautifulSoup(res.text, 'html.parser')
            amazon_page = soup.select('.a-color-base.a-text-normal')
            amazon_page_length = int(len(amazon_page))
            for i in range(0, amazon_page_length):
                name = name.upper()
                amazon_name = soup.select(
                    '.a-color-base.a-text-normal')[i].getText().strip().upper()
                ren = "Renewed"
                if (name in amazon_name[0:20]) and (ren not in amazon_name[0:20]):
                    amazon_name = soup.select(
                        '.a-color-base.a-text-normal')[i].getText().strip().upper()
                    amazon_price = soup.select(
                        '.a-price-whole')[i].getText().strip().upper()
                    a_rating = soup.select('.a-icon-alt')[4].getText()
                    print("Amazon:")
                    print(amazon_name)
                    print("₹" + amazon_price)
                    print(a_rating)
                    print("-----------------------")
                    break
                else:
                    i += 1
                    i = int(i)
                    if i == amazon_page_length:
                        print("amazon : No product found!")
                        print("-----------------------")
                        amazon_price = 'No Product Price Found'
                        infor.append(amazon_price[0:2])
                        break
            infor.append(amazon_name)
            infor.append("₹" + amazon_price)
            rate.append(a_rating)
        except:
            print("amazon: No product found!")
            print("-----------------------")
            amazon_price = 'Product Price Not found!'
            infor.append(amazon_price)
            return render(request, 'price/next.html',
                          {'expectF': infor[2:4], 'expectA': infor[0:1], 'expectA1': infor[1:2]})

        print(infor)

    if flipkart == "on":
        try:
            name = request.GET.get("text", "default")
            name1 = name.replace(" ", "+")  
            name2 = name.replace(" ", "+")
            flipkart = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
            res = requests.get(
                f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off',
                headers=headers)
            print("\nSearching in flipkart....")
            soup = BeautifulSoup(res.text, 'html.parser')
            flipkart_name = soup.select('._4rR01T')[0].getText().strip()
            flipkart_name = flipkart_name.upper()
            if name.upper() in flipkart_name:
                flipkart_price = soup.select('._1_WHN1')[0].getText().strip()
                flipkart_name = soup.select('._4rR01T')[0].getText().strip()
                f_rating=soup.select('._3LWZlK')[0].getText().strip() + ' out of 5 stars'
                print("Flipkart:")
                print(flipkart_name)
                print(flipkart_price)
                print(f_rating)
                print("-----------------------")
                infor.append(flipkart_name)
                infor.append(flipkart_price)
                rate.append(f_rating)
            else:
                print("Flipkart:No product found!")
                print("-----------------------")
                flipkart_price = 'No Product Price Found'
                infor.append(flipkart_price)
        except:
            print("Flipkart:No product found!")
            print("-----------------------")
            flipkart_price = 'Product Price Not found!'
            infor.append(flipkart_price)
            return render(request, 'price/next.html',
                          {'expectF': infor[2:], 'expectA': infor[0:1], 'expectA1': infor[1:2]})

    return render(request, 'price/next.html', {'a': infor[0], 'b': infor[1], 'c': infor[2], 'd': infor[3], 'e': infor[4:], 'a_rate': rate[0], 'f_rate':rate[1]})
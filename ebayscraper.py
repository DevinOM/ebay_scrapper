from bs4 import BeautifulSoup
import requests


URL_3070 = 'https://www.ebay.com/sch/i.html?_dcat=27386&_fsrp=1&_udlo=500&_nkw=rtx+3070&_sacat=0&_from=R40&LH_ItemCondition=1000&rt=nc&Brand=AORUS%7CASUS%7CEVGA%7CGIGABYTE%7CZOTAC%7CNVIDIA%7CMSI%7CPNY'
URL_3080 = 'https://www.ebay.com/sch/i.html?_dcat=27386&_fsrp=1&_udlo=700&_nkw=rtx+3080&_sacat=0&_from=R40&LH_ItemCondition=1000&rt=nc&Brand=AORUS%7CASUS%7CEVGA%7CZOTAC%7CGIGABYTE%7CMSI%7CNVIDIA'
URL_3090 = 'https://www.ebay.com/sch/i.html?_dcat=27386&_fsrp=1&_udlo=1500&_nkw=rtx+3090&_sacat=0&_from=R40&LH_ItemCondition=1000&rt=nc&Brand=ASUS%7CEVGA%7CGIGABYTE%7CZOTAC%7CPNY%7CNVIDIA%7CMSI'


# Pass in the url to return the html of site
def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


# With the HTML of the site, gather all necessary data and store in a dictionary of lists
def parse(soup):
    results = soup.find_all('div', {'class': 's-item__info clearfix'})  # All entries of items being sold
    print(f'{len(results)} items found')
    # Dictionary that will hold product details
    product_info = {
        'titles': [],  # Product name listed
        'prices': [],  # Product asking price
        'brands': [],  # Brand of GPU
        'conditions': []}  # Condition of GPU

    for item in results:  # Loops through each item
        try:
            title = item.find('h3', {'class': 's-item__title'}).text.replace('New Listing', '')
            price = item.find('span', {'class': 's-item__price'}).text.replace('$', '').replace(',', '')
            brand = item.find('div', {'class': 's-item__subtitle'}).text.rsplit(' · ')[1]
            condition = item.find('div', {'class': 's-item__subtitle'}).find('span', {'class': 'SECONDARY_INFO'}).text
        except AttributeError:
            continue
        except IndexError:
            continue
        else:
            product_info['titles'].append(title)
            product_info['prices'].append(float(price))
            product_info['brands'].append(brand)
            product_info['conditions'].append(condition)
    return product_info


def product_price_lists():
    ebay_3000_prices = {'Averages': {},
                        'Lows': {},
                        'Highs': {}}
    for i in range(3):
        if i == 0:
            url = URL_3070
            model = '3070'
        elif i == 1:
            url = URL_3080
            model = '3080'
        else:
            url = URL_3090
            model = '3090'
        soup = get_data(url)
        my_dict = parse(soup)
        avg_price = 0
        low_price = high_price = my_dict['prices'][0]
        for idx in my_dict['prices']:
            avg_price += idx
            if idx < low_price:
                low_price = idx
            if idx > high_price:
                high_price = idx
        avg_price /= len(my_dict['prices'])
        ebay_3000_prices['Averages'][model] = round(avg_price, 2)
        ebay_3000_prices['Lows'][model] = round(low_price, 2)
        ebay_3000_prices['Highs'][model] = round(high_price, 2)
    return ebay_3000_prices


def models_product_info():
    ebay_3000_prices = {'3070': {},
                        '3080': {},
                        '3090': {}}
    for i in range(3):
        if i == 0:
            url = URL_3070
            model = '3070'
        elif i == 1:
            url = URL_3080
            model = '3080'
        else:
            url = URL_3090
            model = '3090'
        soup = get_data(url)
        ebay_3000_prices[model] = parse(soup)
    return ebay_3000_prices

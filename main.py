from kabum import KabumBot
import api
import time
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

EMAIL, PASSWORD = (os.getenv('EMAIL'), os.getenv('PASSWORD'))

def findCoupon(coupons, couponId):
    for coupon in coupons:
        if coupon['id'] == couponId:
            return coupon

def discountAbsoluteAmount(discount, price):
    if(not discount):
        return 0
    if '%' in discount:
        discountAmount = float(discount[:-1])*price/100**2
    else:
        discountAmount = float(discount)
    return discountAmount

def main():
    coupons = api.get_coupons(bot.retailer_id)
    products = api.get_retailer_products(bot.retailer_id)
    for product in products:
        bot = KabumBot()
        print('produto: ', product['title'], product['html_url'])
        data = {}
        try:
            data['price'] = bot.accessCart(product['html_url'])
            data['available'] = True
            for coupon in coupons:
                if coupon['available']:
                    try:
                        couponAvailable = bot.tryCoupon(coupon['code'])
                        if couponAvailable:
                            print(f'O cupom {coupon["code"]} funciona em {product["title"]}')
                            discountAmount = discountAbsoluteAmount(coupon['discount'], data['price'])
                            print(discountAmount)
                            if product['coupon'] and discountAmount >= discountAbsoluteAmount(product['coupon']['discount'], data['price']) or not product['coupon']:
                                data['coupon_id'] = coupon['id']
                                data['price'] = int(data['price'] - discountAmount*100)
                    except Exception as e:
                        print('erro teste de cupom: ', product['title'])
                    bot.refreshCart() 
        except Exception as e:
            print('Produto indisponível: ', product['title'])
            data['available'] = False
        if 'price'in data and data['price'] != product['price'] or data['available'] != product['available']:
            api.update_product_retailers(product['id'], bot.retailer_id, data).content
        print(data)
        bot.closeBrowser()

if __name__ == '__main__':
    currentDateTime = datetime.now()
    currentHour = currentDateTime.strftime('%H')
    while currentHour != '06':
        print(f'A hora atual é de {currentHour}h. O script encerrará a partir das 3h da manhã e voltará às 5h.')
        start_time = time.time()
        main()
        print(f'Fim da rodada. O tempo de execução foi de {time.time() - start_time} segundos.')
        currentDateTime = datetime.now()
        currentHour = currentDateTime.strftime('%H')
    



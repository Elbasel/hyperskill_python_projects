import requests

def get_rates(currency):
    return requests.get(f'http://www.floatrates.com/daily/{currency}.json').json()


cache = {'usd': get_rates('usd'),
         'eur': get_rates('eur')}


source_currency = input().lower()

while True:
    target_currency = input().lower()

    if not target_currency:
        break

    amount = int(input())

    print('Checking the cache...')

    if target_currency in cache.keys():
        print('Oh! It is in the cache!')
    else:
        print('Sorry, but it is not in the cache!')
        cache[target_currency] = get_rates(target_currency)
    
    rate = cache[target_currency][source_currency]['inverseRate']
    print(f'You received {round(amount * rate, 2)} {target_currency.upper()}')
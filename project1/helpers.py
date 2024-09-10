import requests
import sys
times = 0

while True:
    password = input('What is the password: ')
    if password != 'Bupysafo1':
        times +=1
        if times == 1:
            print("Wrong password, you have 2 more tries")
        elif times == 2:
            print("Wrong password, you have 1 more try")
        elif times == 3:
            sys.exit("To many tries")
    else:
        break

# Define the target currencies list
target_currencies = ['USD', 'BRL', 'EUR', 'CNY','GBP']

# Dictionary to store conversion rates for quick access
conversion_rates = {}

# Global variables to keep track of the base currency and amount
base_currency = 'USD'
base_amount = 1

# Api key
API_KEY = 'd6356125405f6886b3a40b5f'

def main():
    global base_currency, base_amount
    valid_currencies = get_valid_currencies(API_KEY)
    if not valid_currencies:
        print("Failed to fetch valid currencies. Exiting the program.")
        return

    while True:
        update_conversion_rates(base_currency, base_amount)  # Ensure rates are up-to-date with current base currency and amount
        favorites()
        choice = input('Enter option: ')
        if choice == '1':
            calculate(valid_currencies)
        elif choice == '2':
            add_currency_to_favorites(valid_currencies)
        elif choice == '3':
            remove_currency_from_favorites()
        elif choice == '4':
            print('Quitting program.')
            print('')
            print('')
            break
        else:
            print('Invalid option, please try again.')

def get_valid_currencies(api_key):

    API_KEY = 'd6356125405f6886b3a40b5f' #toegevoegd

    url = f'https://v6.exchangerate-api.com/v6/{api_key}/codes'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [currency[0] for currency in data['supported_codes']]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError:
        print("Error decoding JSON response.")
    return []

def update_conversion_rates(base_currency, amount):

    base_currency = 'USD' #toegevoegd

    global conversion_rates
    conversion_rates = {}
    for currency in target_currencies:
        if currency != base_currency:
            rate = get_conversion_rate(base_currency, currency, amount)
            if rate is not None:
                conversion_rates[currency] = rate
        else:
            conversion_rates[currency] = round(amount, 2)

def favorites():
    print('')
    print('')
    print('=====================')
    print(' CURRENCY CALCULATOR ')
    print('=====================')
    for currency in target_currencies:
        rate = conversion_rates.get(currency, 'N/A')
        print(f' {currency}: {rate}')
    print('')
    print('[1] Calculate')
    print('[2] Add currency to favorites')
    print('[3] Remove currency from favorites')
    print('[4] Quit program')
    print('')
    print('')

def calculate(valid_currencies):

    base_amount = 1 #toegevoerg

    global base_currency, base_amount
    from_currency = input('Enter the currency you want to convert from: ').upper()
    if from_currency not in valid_currencies:
        print(f'{from_currency} is not a valid currency.')
        return

    try:
        amount = float(input('Enter the amount to convert: '))
    except ValueError:
        print('Invalid amount entered.')
        return

    # Update the base amount
    base_amount = amount

    # Add the currency to the favorites list if not already present
    if from_currency not in target_currencies:
        target_currencies.append(from_currency)

    # Set the new base currency and update conversion rates
    base_currency = from_currency
    update_conversion_rates(base_currency, base_amount)

def get_conversion_rate(from_currency, to_currency, amount):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data['conversion_rate']
        # Round the result to 2 decimal places
        return round(rate * amount, 2)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError:
        print("Error decoding JSON response.")
    return None

def add_currency_to_favorites(valid_currencies):

    base_amount = 1 #toegevoegd

    global base_amount
    add_cur = input('What currency do you want to add to the favorites list? ').upper()
    if add_cur in valid_currencies:
        if add_cur not in target_currencies:
            target_currencies.append(add_cur)
            # Update conversion rates with the current base currency and amount
            update_conversion_rates(base_currency, base_amount)
            print(f'{add_cur} has been added to the favorites list.')
        else:
            print(f'{add_cur} is already in the favorites list.')
    else:
        print(f'{add_cur} is not a valid currency code.')

def remove_currency_from_favorites():

    global base_currency
    remove_cur = input('What currency do you want to remove from the favorites list? ').upper()
    if remove_cur in target_currencies:
        target_currencies.remove(remove_cur)
        # Remove the conversion rate as well
        if remove_cur in conversion_rates:
            del conversion_rates[remove_cur]
        print(f'{remove_cur} has been removed from the favorites list.')

        if remove_cur == base_currency:
            if target_currencies:
                base_currency = target_currencies[0]
            else:
                base_currency = 'USD'
        update_conversion_rates(base_currency, base_amount)
    else:
        print(f'{remove_cur} is not in the favorites list.')





if __name__ == "__main__":
    main()

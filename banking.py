from random import randint
import sqlite3


def generate_card_number() -> str:
    while True:
        card_num = '400000'
        for _ in range(9):
            card_num += str(randint(0, 9))

        cursor.execute('SELECT number from card')
        numbers = [num[0] for num in cursor.fetchall()]
        if card_num not in map(lambda x: x[:-1], numbers):
            break

    num_list = list(map(int, card_num))
    num_list.reverse()
    sum_digits = 0
    for i, num in enumerate(num_list):
        if i % 2 == 0:
            num *= 2
            if num > 9:
                num -= 9
        sum_digits += num

    check_sum = (sum_digits * 9) % 10
    card_num += str(check_sum)

    return card_num


def generate_pin() -> str:
    pin = ''
    for _ in range(4):
        pin += str(randint(0, 9))

    return pin


def user_exists(card_num: str, pin: str) -> bool:
    cursor.execute(f'SELECT pin FROM card WHERE number = {card_num}')
    db_pin = cursor.fetchone()
    if db_pin is None:
        return False
    if pin == 'locate':
        return True
    if db_pin[0] == pin:
        return True

    return False


def create_user() -> None:
    card_num = generate_card_number()
    pin = generate_pin()
    cursor.execute(f'INSERT INTO card VALUES ({id}, {card_num}, {pin}, 0);')
    connection.commit()
    print('Your card has been created', 'Your card number:', card_num,
          'Your card PIN:', pin, sep='\n')


def valid_checksum(num):
    digits = [int(x) for x in num]
    digits.reverse()

    check_sum = 0
    for i, d in enumerate(digits):
        if i % 2 != 0:  # double every right most digits starting from the right
            d *= 2
        if d > 9:  # add the individual digits to the checksum
            check_sum += d // 10
            check_sum += d % 10
        else:
            check_sum += d

    if check_sum % 10 == 0:
        return True
    else:
        return False


connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')

id = 0

while True:
    print('1. Create an account', '2. Log into account', '0. Exit', sep='\n')
    command = input()
    print()

    if command == '0':
        break
    elif command == '1':
        create_user()
        id += 1
    elif command == '2':
        print('Enter your card number:')
        user_card_number = input()
        print('Enter your PIN:')
        pin_input = input()

        if not user_exists(user_card_number, pin_input):
            print('\nWrong card number or PIN!')
        else:
            print('\nYou have successfully logged in!\n')
            while True:
                cursor.execute(f'SELECT balance FROM card WHERE number == {user_card_number}')
                balance = cursor.fetchone()[0]
                print('1. Balance', '2. Add income', '3. Do transfer', '4. Close account', '5. Log out', '0. Exit', sep='\n')
                login_command = input()
                print()
                if login_command == '1':
                    print(f'Balance: {balance}')
                elif login_command == '2':
                    print('Enter income:')
                    income = float(input())
                    cursor.execute(f'UPDATE card SET balance = balance + {income} WHERE number = {user_card_number}')
                    print('Income was added!')
                elif login_command == '3':
                    while True:
                        print('Transfer', 'Enter card number:', sep='\n')
                        trnsfr_card_num = input()
                        if not valid_checksum(trnsfr_card_num):
                            print('Probably you made a mistake in the card number. Please try again!')
                            break
                        elif not user_exists(trnsfr_card_num, 'locate'):
                            print('Such a card does not exist.')
                            break

                        print('Enter how much money you want to transfer:')
                        trnfr_amount = int(input())
                        if trnfr_amount > balance:
                            print('Not enough money!')
                            break
                        else:
                            cursor.execute(f'UPDATE card SET balance = balance - {trnfr_amount} WHERE number = {user_card_number}')
                            cursor.execute(f'UPDATE card SET balance = balance + {trnfr_amount} WHERE number = {trnsfr_card_num}')
                            print('Success!')
                            break
                elif login_command == '4':
                    cursor.execute(f'DELETE FROM card where number = {user_card_number}')
                    connection.commit()
                    print('The account has been closed!')
                    break

                elif login_command == '5':
                    print('You have successfully logged out!')
                    break
                elif login_command == '0':
                    exit()
                print()
                connection.commit()

    print()

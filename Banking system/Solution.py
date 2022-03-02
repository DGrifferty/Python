import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor

# conn.execute('''CREATE TABLE card
# (id INTEGER PRIMARY KEY NOT NULL,
# number TEXT NOT NULL,
# pin TEXT NOT NULL,
# balance INTEGER DEFAULT 0);''')

def get_data():

    cursor = conn.execute("SELECT id, number, pin, balance from card")
    # data.fetchall()
    id_lst, card_num_lst, pin_lst, balance_lst = [], [], [], []

    for row in cursor:
        id_lst.append(row[0])
        card_num_lst.append(row[1])
        pin_lst.append(row[2])
        balance_lst.append(row[3])

    # print(id_lst)
    # print(card_num_lst)
    # print(pin_lst)
    # print(balance_lst)

    return id_lst, card_num_lst, pin_lst, balance_lst


def create_card_number():

    bin = "400000"
    account_identifier = ""
    for i in range(9):
        account_identifier = account_identifier + str(random.randint(0, 9))

    check_sum = luhn_algorthm_generate(int(bin + account_identifier))

    return int(bin + account_identifier + check_sum)


def create_card_pin():
    return random.randint(1000, 9999)


def create_an_account():
    print('Your card has been created.')

    print('Your card number is:')
    Card_number = create_card_number()
    print(Card_number)

    print('Your pin is: ')
    pin = create_card_pin()
    print(pin)

    id_lst = get_data()[1]

    new_id = len(id_lst)

    conn.execute(f'INSERT INTO card VALUES ({new_id}, {Card_number}, {pin}, 0)')
    conn.commit()

    return Card_number, pin


def log_in():

    id_lst, card_num_lst, pin_lst, balance_lst = get_data()
    user_card_num = input('Enter card number: ')

    if user_card_num in card_num_lst:
        card_num_index = card_num_lst.index(user_card_num)
    else:
        card_num_index = None

    user_pin = input('Enter pin: ')
    if user_pin in pin_lst:
        pin_index = pin_lst.index(user_pin)
    else:
        pin_index = False

    if pin_index == card_num_index:
        print('You have successfully logged in!')
        return True, id_lst[pin_index]
    else:
        print('Wrong pin/card num combination.')
        return False, None


def luhn_algorthm_generate(card_num: int) -> bool:
    """generates a card num to
    correspond with the luhn algorithm"""

    card_num_lst = [int(x) for x in str(card_num)]

    # Mutiplying odd digits by two
    for index, value in enumerate(card_num_lst):
        if index == 0 or index % 2 == 0:
            # print(index)
            card_num_lst[index] *= 2

        if card_num_lst[index] > 9:
            card_num_lst[index] -= 9

    if sum(card_num_lst) % 10 == 0:
        return str(0)
    else:
        return str(10 - sum(card_num_lst) % 10)


def luhn_algorthm_check(card_num: int) -> bool:
    """Checks that a user entered card num
    corresponds with the luhn algorithm"""

    card_num_lst = [int(x) for x in str(card_num)]
    last_digit = card_num_lst[-1]

    card_num_lst[-1] = 0
    # Mutiplying odd digits by two
    for index, value in enumerate(card_num_lst):
        if index == 0 or index % 2 == 0:
            card_num_lst[index] *= 2

        if card_num_lst[index] > 9:
            card_num_lst[index] -= 9

    if (sum(card_num_lst) + last_digit) % 10 == 0:
        return True
    else:
        return False


card_num = False
pin = False
logged_in = False

while True:

    if logged_in == False:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        user_choice = int(input('>'))

        if user_choice == 1:
            card_num, pin = create_an_account()
            # if luhn_algorthm_check(card_num):
            #     print('True')
            # else:
            #     print('False')

            continue

        elif user_choice == 2:
            logged_in = log_in()
            if logged_in[0] == True:
                user_id = logged_in[1]
                logged_in = True
            else:
                logged_in = False
            continue

        elif user_choice == 0:
            exit()

    if logged_in == True:
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        user_choice = int(input('>'))

        id_lst, card_num_lst, pin_lst, balance_lst = get_data()

        if user_choice == 1:
            print(balance_lst[user_id])  # Create add balance function
            continue

        elif user_choice == 2:
            income = int(input('Type income to add: '))
            total_balance = balance_lst[user_id] + income
            conn.execute(f'UPDATE card set balance = {total_balance} where id = {user_id}')
            conn.commit()
            print('Income was added')

        elif user_choice == 3:

            transfer_card_num = input('Enter card number to transfer to: ')

            if transfer_card_num == card_num_lst[user_id]:
                print('You can\'t transfer money to the same account!')
                continue
            elif not luhn_algorthm_check(transfer_card_num):
                print('Probably you made a mistake in the card number. Please try again!')
                continue
            elif transfer_card_num not in card_num_lst:
                print('Such a card does not exist')
                continue


            user_balance = balance_lst[user_id]
            transfer_amount = int(input('Type amount that you want to transfer: '))

            if transfer_amount > user_balance:
                print('Not enough money!')
                continue

            new_balance = user_balance - transfer_amount
            conn.execute(f'UPDATE card set balance = {new_balance} where id = {user_id}')

            transfer_id = card_num_lst.index(transfer_card_num)
            transfer_user_balance = balance_lst[transfer_id] + transfer_amount
            conn.execute(f'UPDATE card set balance = {transfer_user_balance} where id = {transfer_id}')

            conn.commit()

            print('Success!')

        elif user_choice == 4:

            conn.execute(f'DELETE FROM card WHERE id = {user_id}')
            conn.commit()

            print('The account has been closed!')


        elif user_choice == 5:
            logged_in = False
            print('You have successfully logged out!')
            continue

        elif user_choice == 0:
            exit()

print('Goodbye!')
print(conn.total_changes)
conn.commit()
conn.close()

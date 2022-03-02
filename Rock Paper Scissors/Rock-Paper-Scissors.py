import random


def winner(user, comp, choices):
    draw = False

    if comp == user:
        print(f'There is a draw ({comp})')
        draw = True
        return 50

    # beat half the list and lose to the other half

    if not draw:

        user_index = choices.index(user)
        comp_index = choices.index(comp)

        max = len(choices) - 1
        half = int(max/2)
        lose_to = list()

        for i in range(half):

            if user_index + 1 + i > max:
                lose_to.append(0 + i)
            else:
                lose_to.append(user_index + 1 + i)

        if comp_index in lose_to:
            print(f'Sorry but the computer chose {comp}')
            return 0
        else:
            print(f'Well done the computer chose {comp} and failed')
            return 100


        # if comp == 'rock':
        #     if user == 'paper':
        #         print(f'Well done the computer chose {comp} and failed')
        #         return 100
        #     else:
        #         print(f'Sorry but the computer chose {comp}')
        #         return 0
        #
        # elif comp == 'scissors':
        #     if user == 'rock':
        #         print(f'Well done the computer chose {comp} and failed')
        #         return 100
        #     else:
        #         print(f'Sorry but the computer chose {comp}')
        #         return 0
        #
        # elif comp == 'paper':
        #     if user == 'scissors':
        #         print(f'Well done the computer chose {comp} and failed')
        #         return 100
        #     else:
        #         print(f'Sorry but the computer chose {comp}')
        #         return 0


if __name__ == '__main__':

    username = input('Enter your name: ').title()

    print(f'Hello, {username}')
    choices = input()
    if choices:
        choices = choices.split(',')
    else:
        choices = 'paper,scissors,rock'.split(',')
    print('Okay, let\'s start')
    with open('rating.txt', 'r+') as f:
        rating = f.read()
        rating = [s.strip() for s in rating.splitlines()]
        ratings = []
        for s in rating:
            ratings.append(s.split(' '))
        ratings = dict(ratings)

        if username in ratings.keys():
            user_rating = int(ratings[username])

        else:
            f.writelines(f'{username} 0')
            user_rating = 0
            ratings[username] = ' 0'

    while True:

        while True:
            user_choice = input().lower()
            if user_choice in choices:
                break
            elif user_choice == '!rating':
                print(f'Your rating: {user_rating}')
            elif user_choice == '!exit':
                print('Bye!')
                with open('rating.txt', 'w') as f:
                    for key in ratings.keys():
                        f.writelines(f'{key} {ratings[key]}\n')
                quit()
            else:
                print('Invalid input')

        comp_choice = random.choice(choices)
        user_rating += winner(user_choice, comp_choice, choices)
        ratings[username] = user_rating

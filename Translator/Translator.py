import requests
from bs4 import BeautifulSoup
from typing import Dict
import sys


def print_dic(dic: Dict) -> str:
    """Allows you to print a dictionary in a cleaner way"""

    values = list(dic.values())
    keys = list(dic.keys())

    string = ''

    for i in range(len(keys)):

        if i == len(keys) - 1:
            string += f'{keys[i]}. {values[i]}.'
        else:
            string += f'{keys[i]}. {values[i]}\n'

    print(string)


def get_tran_info():
    print('Hello, welcome to the translator. languages supported are as follows:')
    language_dict = {'1': 'Arabic', '2': 'German', '3': 'English', '4': 'Spanish',
                     '5': 'French', '6': 'Hebrew', '7': 'Japanese', '8': 'Dutch',
                     '9': 'Polish', '10': 'Portuguese', '11': 'Romanian', '12': 'Russian',
                     '13': 'Turkish'}

    print_dic(language_dict)

    lanfrom = input('Type the number of your language: ')

    if lanfrom in language_dict.keys():
        lanfrom = language_dict[lanfrom]
    else:
        print(f'Sorry, that option is not available.')
        quit()

    lanto = input("Type the number of the language you want to translate to or"
                  " '0' to translate to all languages: ")
    if lanto in language_dict.keys():
        lanto = language_dict[lanto]
    elif lanto == '0':
        lanto = 0
    else:
        print(f'Sorry, that option is not available.')
        quit()

    user_translate = input('Type the word you want to translate: ')

    return user_translate, lanfrom, lanto


def generate_url(user_translate, lanfrom, lanto):
    url = 'https://context.reverso.net/translation/'
    url += f'{lanfrom.lower()}-{lanto.lower()}/{user_translate}'
    print(url)
    return url


def request(url, first):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh)'}
    r = requests.get(url, headers=headers)
    if first:

        if r:
            print(str(r.status_code) + ' OK' + '\n')
        else:
            print(str(r.status_code) + ' fail')
            if r.status_code == 404:
                print(f'Sorry, unable to find {url.split("/")[-1]}')
            else:
                print('Something is wrong with your internet connection')
            quit()

    return r


def get_trans(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    translations = soup.find_all(['div', 'a'], {'class': 'dict'})
    examples = soup.find_all('div', {'class': ['src', 'trg']})

    return translations, examples


def format_translations(translations, no_of_examples):
    translations = [t.text.strip('\n ') for t in translations]
    forbidden = '"[]'
    f_translations = ''
    for index, word in enumerate(translations):
        for char in forbidden:
            if char in word:
                translations[index] = word.replace(char, '')

    for i in range(no_of_examples):
        try:
            f_translations += translations[i] + '\n'
        except:
            break
    return f_translations


def format_examples(examples, no_of_examples):
    examples = [e.text.strip('\n ') for e in examples if e.text.strip()]
    forbidden = '"[]'
    f_examples = ''
    for index, sentence in enumerate(examples):
        for char in forbidden:
            if char in sentence:
                examples[index] = sentence.replace(char, '')

    for i in range(0, no_of_examples * 2, 2):
        try:
            f_examples += examples[i] + ':' + '\n'
            f_examples += examples[i + 1] + '\n' + '\n'

        except:
            break

    return f_examples


def print_to_file(f, user_translate, lanfrom, lanto, first):
    url = generate_url(user_translate, lanfrom, lanto)
    r = request(url, first)
    translations, examples = get_trans(r)
    no_of_examples = 5
    f.write(f'{lanto} Translations: \n')
    f.write(format_translations(translations, no_of_examples) + '\n')
    f.write(f'{lanto} Examples: \n')
    f.write(format_examples(examples, no_of_examples) + '\n')


if __name__ == '__main__':
    language_dict = {'1': 'Arabic', '2': 'German', '3': 'English', '4': 'Spanish',
                     '5': 'French', '6': 'Hebrew', '7': 'Japanese', '8': 'Dutch',
                     '9': 'Polish', '10': 'Portuguese', '11': 'Romanian', '12': 'Russian',
                     '13': 'Turkish'}
    if len(sys.argv) > 1:
        if len(sys.argv) != 4:
            print('Error')
        else:
            args = sys.argv
            lanfrom = args[1]
            if lanfrom not in language_dict:
                print(f'Sorry, the program does\'nt support {lanfrom}')
            lanto = args[2]
            if lanto not in language_dict:
                print(f'Sorry, the program does\'nt support {lanto}')
            if lanto == 'all':
                lanto = 0
            user_translate = args[3]
    else:
        user_translate, lanfrom, lanto = get_tran_info()

    first = True
    with open(f'{user_translate}.txt', 'w', encoding='utf-8') as f:
        if lanto != 0:
            print_to_file(f, user_translate, lanfrom, lanto, first)

        elif lanto == 0:
            for lanto in language_dict.values():
                if lanto != lanfrom:
                    print_to_file(f, user_translate, lanfrom, lanto, first)
                    first = False

    with open(f'{user_translate}.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            print(line, end='')

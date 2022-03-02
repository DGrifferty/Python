import requests
from bs4 import BeautifulSoup


def language_direction() -> str:
    # to later be used as language from and to
    while True:
        languages = {'fr': 'french',
                     'en': 'english'}
        lanto = ''
        # lanfrom = input('Type \'en\' if you want to translate from English'
        #   '\n or \'fr\' if you want to translate from french:')
        lanfrom = input('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
        # print(f'lanto {lanto}')

        if lanfrom == 'fr':
            lanto += 'en'
        else:
            lanto += 'fr'
        # print(f'lanfrom {lanfrom}')

        # if lanto == lanfrom:
        #     print('That would be pointless!')
        #     continue
        # if lanto or lanfrom not in languages.keys:
        #     continue
        # else:
        return languages[lanto], languages[lanfrom]


def to_translate(lanfrom) -> str:
    # To be used to fulfill any later conditions on user input

    user_translate = input('Type the word you want to translate: ')

    print(f'You chose fr as a language to translate {user_translate} to.')

    return user_translate


def generate_url():
    lanto, lanfrom = language_direction()
    words = to_translate(lanfrom)
    url = 'https://context.reverso.net/translation/'
    url += lanfrom + '-' + lanto + '/' + words
    return url


def request() -> str:
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh)'}
    r = requests.get(generate_url(), headers=headers)
    if r:
        print(str(r.status_code) + ' OK')
    else:
        print(str(r.status_code) + ' fail')
    return r


if __name__ == '__main__':
    r = request()
    soup = BeautifulSoup(r.content, 'html.parser')

    # words = soup.find_all('a', class_='translation')
    # examples = soup.find_all('div', {'class': ['src', 'trg']})

    print('Translations')

    print([w.text.strip('\n ') for w in soup.find_all(['div', 'a'], {'class': 'dict'})])
    print([e.text.strip('\n ') for e in soup.find_all('div', {'class': ['src', 'trg']})])

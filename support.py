import logging
import requests
import re
from bs4 import BeautifulSoup

conf = open('config', 'r').readline()
token = re.search('token=\'(\S+)\'', conf).group(1)
server_id = re.search('server_id=\'(\S+)\'', conf).group(1)

def log(app, logfile):
    logger = logging.getLogger(app)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger


def look_up_dict(word):
    response = requests.get('http://www.dictionary.com/browse/{}?s=t'.format(word.lower()))
    response = BeautifulSoup(response.text, 'html.parser')

    pronun = response.find(class_='pron spellpron')
    pronun = ''.join(list(pronun.stripped_strings))

    defset = response.find(class_='def-set')
    defin = ''
    for tag in defset.stripped_strings:
        if tag[0].isdigit():
            defin += '\n'
        else:
            defin += tag

    example = response.find(class_='partner-example-text')
    if example is not None:
        example = ' '.join(list(example.stripped_strings)).replace('\xa0', ' ')
    else:
        example = ''

    post = '**{}** *{}*'.format(word, pronun[1:-1]) + defin + '\n`{}`'.format(example)
    return post


if __name__ == '__main__':
    print(look_up_dict('jewel'))
    print(token)

from urllib import request
import webbrowser  # to open the QR web site
import requests # to retrieve data from web site
import time
import os
import random
import string
# import telebot // not relevant for my assigenment

from rich import print
from dotenv import load_dotenv
from rich.console import Console
from ldap3 import Server, Connection

# Constants

load_dotenv()

PASS = 1234 # sample



console = Console()

 # Approved users, username: telegram_id
#aproved_users = {
#     'read-only-admin': TG_UID,  # Value: Telegram UID (int)
#}

print("PASS=",PASS)

def user_login(username: str, password: str) -> bool:
    """
    First auth of the user

    Args:
        username ([str]): [Username]
        password ([str]): [Password]

    Returns:
        [boll]: [True if user is aproved]
    """
    return username == 'read-only-admin' and password == 'password'


def telegram_bot(api_token: str):
    """
    Function to create a bot, generate random code and send it to the user

    Args:
        api_token ([str]): [TG Bot Api Token]
    """
    global PASS
    bot = telebot.TeleBot(api_token)
    PASS = int(generate_random_code())

    bot.send_message(search_in_dict(aproved_users, username), PASS)


def search_in_dict(dct: dict, key: str) -> int:
    """
    Search a user in a dict and return the his TG UID

    Args:
        dct ([dict]): [dictionary of users]
        key ([str]): [username]

    Returns:
        [type]: [description]
    """
    for k, v in dct.items():
        if k == key:
            return v


def generate_random_code() -> str:
    """
    Generate a random MFA code

    Returns:
        [int]: [random code]
    """
    return ''.join(random.choice(string.digits) for _ in range(6))


def connect_to_ldap(url: str, username: str, password: str):
    """
    Connect to LDAP server and print the entries

    Args:
        url ([str]): [LDAP server url]
        username ([str]): [Username]
        password ([str]): [Password]
    """
    server = Server(url)
    with Connection(server, f'cn={username},dc=example,dc=com', f'{password}') as conn:
        conn.search('dc=example,dc=com', '(objectClass=*)', attributes=['*'])
        for entry in conn.entries:
            print(entry)


if __name__ == '__main__':
    url = input('Enter LDAP URL (ldap.forumsys.com): \n>>> ')
    username = input('Enter username (read-only-admin): \n>>> ')
    password = input('Enter password (password): \n>>> ')

    if user_login(username, password):
        console.print(f'{username} is logged in!')
        #telegram_bot(TOKEN)
        # the url go generate a Google Authentication QR 6 digits number.
        # SecretCode - A secret code that only you know
        QR_url ='https://www.authenticatorapi.com/pair.aspx?AppName=EfyEisikovits&AppInfo='+username+'&SecretCode=1234'
        
        print('Enter the code  from the QR (opened in a new browser tab):')
        time.sleep(3) # Sleep for 3 seconds
        
        #code  = int(input('Enter the code  from the QR (opened in a new browser tab): \n>>> '))
        webbrowser.open(QR_url)  # opens the QR in a new browser tab
        
        code  = int(input('>>>'))
        #code = int(input('Enter the code from auth bot:\n'))

        validateQR_url='https://www.authenticatorapi.com/Validate.aspx?Pin='+str(code)+'&SecretCode=1234'
        x = requests.post(validateQR_url)
        print(x.text)
        if x.text == 'True':
            console.print('You are logged in!')
            if connect_to_ldap(url, username, password):
                console.print('Successfully connected to LDAP!')
            else:
                console.print('Failed to connect to LDAP!')
        else:
            console.print('Wrong code!')
    else:
        console.print('Wrong username or password!')
        exit()
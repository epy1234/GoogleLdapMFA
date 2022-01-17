from urllib import request
import webbrowser  # to open the QR web site
import requests # to retrieve data from web site
import time
import os
import random
import string

from rich import print
from dotenv import load_dotenv
from rich.console import Console
from ldap3 import Server, Connection


load_dotenv()

console = Console()


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
        appName="OpenLdap"
        PASS = generate_random_code()
        # the url go generate a Google Authentication QR 6 digits number.
        # SecretCode - A secret code that only you know
        QR_url =f'https://www.authenticatorapi.com/pair.aspx?AppName={appName}&AppInfo={username}&SecretCode={PASS}'
        
        print('Enter the code  from the QR (opened in a new browser tab):')
        time.sleep(3) # let the user see the last message
        
        #code  = int(input('Enter the code  from the QR (opened in a new browser tab): \n>>> '))
        webbrowser.open(QR_url)  # opens the QR in a new browser tab
        
        code  = int(input('>>>'))
        #code = int(input('Enter the code from auth bot:\n'))

        validateQR_url=f'https://www.authenticatorapi.com/Validate.aspx?Pin={code}&SecretCode={PASS}'
        validate_qr = requests.post(validateQR_url) # text value = 'True' or 'False'
        print(validate_qr.text)
        if validate_qr.text == 'True':
            console.print('Authentication succeeded, you are logged in!')
            # if connect_to_ldap(url, username, password):
            #     console.print('Successfully connected to LDAP!')
            # else:
            #     console.print('Failed to connect to LDAP!')
        else:
            console.print('Authentication failed, wrong code!')
    else:
        console.print('Wrong username or password!')
        exit()
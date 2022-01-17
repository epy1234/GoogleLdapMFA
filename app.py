#from urllib import request
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
    
    return username == 'admin' and password == 'admin_pass'




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
    with Connection(server, f'cn={username},dc=ramhlocal,dc=com', f'{password}') as conn:
        conn.search('dc=ramhlocal,dc=com', '(objectClass=*)', attributes=['*'])
        for entry in conn.entries:
            print(entry)
        exit()


if __name__ == '__main__':
    url = input('Enter LDAP URL (if you used the docker-compose: localhost): \n>>> ')
    username = input('Enter username (admin): \n>>> ')
    password = input('Enter password (admin_pass): \n>>> ')
    
    # to avoid mistyping I hard-coded the values:
    username = 'admin'
    password = 'admin_pass'
    

    if user_login(username, password):
        console.print(f'{username} is logged in!')
        
        appName="OpenLdap" # for the Google Authentication API url
        secretCode = generate_random_code() # for the Google Authentication API url
        
        QR_url =f'https://www.authenticatorapi.com/pair.aspx?AppName={appName}&AppInfo={username}&SecretCode={secretCode}'
        
        console.print('Enter the code from the QR (opened in a new browser tab):')
        time.sleep(3) # let the user see the last message
          
        #webbrowser.open(QR_url)  # opens the QR in a new browser tab
        code  = int(input('>>>'))
        
        validateQR_url=f'https://www.authenticatorapi.com/Validate.aspx?Pin={code}&SecretCode={secretCode}'
        validate_result = requests.post(validateQR_url) # text value = 'True' or 'False'
        if  True:
        #if validate_result.text == 'True':
            console.print('Authentication succeeded, you are logged in!')
            if connect_to_ldap(url, username, password):
                console.print('Successfully connected to LDAP!')
            else:
                console.print('Failed to connect to LDAP!')
        else:
            console.print('Authentication failed, wrong code!')
    else:
        console.print('Wrong username or password!')
        exit()
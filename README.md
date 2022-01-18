#### LDAP MFA Demo code
- Python Script that simulates a user login and performs authentication via Google Authentication MFA.   
- Once the authentication is complete, the script will connect to `localhost` and pull data to the terminal.
- First run `docker-compose up` to spin up an OpenLdap docker. It will run on your localhost:80.
- You can log in and add users:
- Login DN: `cn=admin,dc=ramhlocal,dc=com`
- Password: `admin_pass`
- run `pip install -r requirements.txt`
- Run `app.py` 

Property  | Value
----------|---------------
server    | localhost
user      | admin
password  | admin_pass

### Python libraries used in this script:

Library           | Link                                          | Description
------------------|-----------------------------------------------|--------------------------------------------
rich              | https://github.com/willmcgugan/rich           | Rich is a Python library for rich text and beautiful formatting in the terminal.
dotenv            | https://github.com/theskumar/python-dotenv    | Python-dotenv reads key-value pairs from a `.env` file and can set them as environment variables.
ldap3             | https://github.com/cannatag/ldap3             | Perform a connection via ldap


## Usage:
[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/nirgeier/LdapMFA.git)
### **<kbd>CTRL</kbd> + click to open in new window**  ﻿# GoogleLdapMFA

Original code is with the help of https://github.com/nirgeier/LdapMFA.git

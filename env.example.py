# Configuration file
# To obtain "client_id" and "login_company", contact your ConnectWise administrator or the relevant team members.
# This file should be named config.py and placed in the same directory as the main script.
CONNECTWISE_BASE_URL = "API URL for Connectwise goes here"
CLIENT_ID = "paste_your_client_id_here"
LOGIN_COMPANY = "paste_your_login_company_here"

# To obtain "public_key" and "private_key":
# 1. In ConnectWise, navigate to "My Account" > "API Keys.
# 2. Click the plus (+) icon, enter a description (e.g., "Label Printing"), and save.
# 3. Copy the displayed public and private keys into the fields below (between the quotes), save the file, and close it.

PUBLIC_KEY = "paste_your_public_key_here"
PRIVATE_KEY = "paste_your_private_key_here"

# This must match the name of the printer in your Printers & Scanners settings in Windows.
PRINTER_NAME = "paste_your_printer_name_here"
BASE_DIR = "Directory of Project"

# Edit these as needed, but these are the default file names for the templates.
TEMPLATE_NORMAL = "ETS EQUIPMENT SHEET TEMPLATE - Normal.docx"
TEMPLATE_LAPTOP = "ETS EQUIPMENT SHEET TEMPLATE - Laptop.docx"
TEMPLATE_FILLED = "ETS EQUIPMENT SHEET - Filled.docx"

SECRET_KEY = "paste_secret_key_here" # Run "$ python -c 'import secrets; print(secrets.token_hex())'" to get one
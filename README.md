## Blocklist-Frontend
The frontend for the update-blocklist script.

# Prerequisites
Clone the repository
```bash
git clone https://github.com/FakeWickey/Update-Blocklist-Frontend.git
```

The project uses flask, so make sure to install it with
```bash
pip install flask
```

Install & Setup mySQL
Create a database and a user with access to that database
Add the database credentials to the config.ini file

Run the database migrations with:
```bash
flask db upgrade
```

Use the GeneratePasswordHash.py script to receive a password hash for the functionality. Make sure to set the salt and pepper values in the ini file before you create the hash.

# How to use & How it works
Enable database mode from update-blocklist repo's .ini file

The project uses a web framework called Flask to render and operate the website.
The Update-blocklist script gathers domains to block in your LAN
The domains are saved in a mySQL database, and that is also read by the update-blocklist script

# Reasons for creating the frontend & Why to use it
- To control functionality, like update-blocklist script behaviour, from the browser.
- And overall, ease of use!

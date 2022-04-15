
# Blogify

A simple Blogify site using Flask (For Flask Workshop)


## Installation

Prerequisite: Python Installed

Navigate to the folder and double click the setup.bat to setup the virtual environment and install the requirements using pip.

To activate the venv, open terminal the same folder and run the command
```
.\venv\Scripts\activate
```

Alternatively, you can manually install the requirements by navigating to the folder and running the following command:

```bash
pip install -r requirements.txt
```

To setup the database, run the following commands:
```
flask db init
flask db migrate -m "first migration"
flask db upgrade
```

Finally to run the app:
```
python app.py
```    
## Authors

- [@shiroyasha9](https://github.com/shiroyasha9)
- [@Roy6801](https://github.com/Roy6801)


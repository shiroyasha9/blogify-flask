pip install -r requirements.txt
flask db init
flask db migrate -m "fm"
flask db upgrade
code .

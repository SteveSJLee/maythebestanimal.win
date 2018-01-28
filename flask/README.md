This is the Animal-Voting Flask application.

To run it on your local system:

Please have python's virtualenv tool installed before beginning.

1) Export the app configuration information from your local MySQL instance; e.g

  export FLASK_DB_NAME=main
  export FLASK_DB_USER=root
  export FLASK_DB_HOST=127.0.0.1
  export FLASK_DB_PASS=password123
  export FLASK_SECRET_KEY=123

2) Create a virtualenv and install Ansible packages:
  virtualenv --python=python3 venv && . venv/bin/activate
  pip install -r requirements.txt

3) Run install_db_tables.sh to connect to the database and create the database tables

4) Run python main.py to start the app on localhost.


If you want to run the app in a Docker container:
Please have python's virtualenv tool and Docker installed before beginning.

1) Create a MariaDB container using the following:
    docker run -d -e MYSQL_ROOT_PASSWORD=password123 -e MYSQL_DATABASE=main --name mariadb mariadb:10.3.4

2) Build the container and tag it as 'animalvoting'
    docker build -t animalvoting .

3) Start the Flask container and link it to the database:
    docker run -d --name animalvoting -p 5000:8000 -e FLASK_SECRET_KEY='123' -e FLASK_DB_NAME='main' -e FLASK_DB_USER='root' -e FLASK_DB_PASS='password123' -e FLASK_DB_HOST='mysql' --link mariadb:mysql animalvoting

4) The app will now be available on localhost, port 5000.



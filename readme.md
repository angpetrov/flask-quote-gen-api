## Setting up the Flask App and PostgreSQL Database

1.  Clone the repository from GitHub: `git clone https://github.com/angpetrov/flask-quote-gen-api.git`
2.  Navigate to the project directory: `cd flask-quote-gen-api`
3.  Create a virtual environment for the project: `python3 -m venv venv`
4.  Activate the virtual environment: `source venv/bin/activate`
5.  Install the required packages: `pip install -r requirements.txt`
6.  Set the environment variable for the Flask app: `export FLASK_APP=app.py`
7.  Create a new PostgreSQL database instance, and note the database credentials.
8.  Update the `app.py` file with the PostgreSQL database URI and secret key:

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<password>@<hostname>:<port>/<database_name>' 
app.config['SECRET_KEY'] = '<secret_key>'
```

9.  Set up the database by running the following commands:
- `flask db init`
- `flask db migrate`
- `flask db upgrade`


## Running the Flask App

1.  Activate the virtual environment: `source venv/bin/activate`
2.  Set the environment variable for the Flask app: `export FLASK_APP=app.py`
3.  Start the Flask app: `flask run`

## Using the Flask App

1.  Open a web browser and navigate to `http://localhost:5000/`.
2.  You should see a random quote from the database displayed on the screen.

## Using the API
1.  To create a new quote, send a `POST` request to `http://localhost:5000/quotes` with the following JSON payload:
```
POST /quotes HTTP/1.1
Host: localhost:5000
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
Content-Type: application/json

{
  "quote": "To be or not to be, that is the question.",
  "author": "William Shakespeare"
}
```
2.  To get all quotes for the currently authenticated user, send a `GET` request to `http://localhost:5000/quotes`.
3.  To get a specific quote by ID, send a `GET` request to `http://localhost:5000/quotes/<quote_id>`.
4.  To update a specific quote by ID, send a `PUT` request to `http://localhost:5000/quotes/<quote_id>` with the following JSON payload:
```
{
    "quote": "The greatest glory in living lies not in never falling, but in rising every time we fall.",
    "author": "Nelson Mandela"
}
```
5.  To delete a specific quote by ID, send a `DELETE` request to `http://localhost:5000/quotes/<quote_id>`.


Note: To use the API, you need to provide authentication credentials with your request. You can do this by including an `Authorization` header in your request with the value `Basic <base64-encoded-username-and-password>`. You can generate a password hash with the following short code:

```
from werkzeug.security import generate_password_hash

password = 'your password here'
hashed_password = generate_password_hash(password)

print(hashed_password)
```

Note: I added the user to the DB manually. In Postgres you can do that by:
```
INSERT INTO "user" (username, password_hash)
VALUES ('newuser', 'passwordhash');
```

## Sample implementation
Implementation of this project can be found here https://quote-generator-cshw.onrender.com/



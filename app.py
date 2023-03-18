from flask import Flask, request
from flask_migrate import Migrate
from models import db, UserModel, QuoteModel
from auth import basic_auth_required
from flask import Flask, request, render_template
from sqlalchemy import func
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://<username>:<password>@<hostname>:<port>/<database_name>"
app.config['SECRET_KEY'] = 'api-test'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/quotes', methods=['POST'])
@basic_auth_required
def create_quote():
    if request.is_json:
        data = request.get_json()
        username = request.authorization.username
        user = UserModel.query.filter_by(username=username).first()
        new_quote = QuoteModel(
            quote=data['quote'],
            author=data.get('author'),
            user_id=user.id
        )
        db.session.add(new_quote)
        db.session.commit()
        return {"message": f"quote {new_quote.quote} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}


@app.route('/quotes', methods=['GET'])
@basic_auth_required
def get_quotes():
    username = request.authorization.username
    user = UserModel.query.filter_by(username=username).first()
    quotes = QuoteModel.query.filter_by(user_id=user.id).all()
    results = [
        {
            "id": quote.id,
            "quote": quote.quote,
            "user_id": quote.user_id,
            "created_at": quote.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        } for quote in quotes]

    return {"count": len(results), "quotes": results}


@app.route('/quotes/<quote_id>', methods=['GET', 'PUT', 'DELETE'])
@basic_auth_required
def handle_quote(quote_id):
    quote = QuoteModel.query.get_or_404(quote_id)

    if request.method == 'GET':
        response = {
            "quote": quote.quote,
            "quote_author": quote.quote_author,
            "user_id": quote.user_id,
            "created_at": quote.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        }
        return {"message": "success", "quote": response}

    elif request.method == 'PUT':
        data = request.get_json()
        username = request.authorization.username
        user = UserModel.query.filter_by(username=username).first()
        if quote.user_id == user.id:
            quote.quote = data['quote']
            quote.quote_author = data.get('quote_author')
            db.session.add(quote)
            db.session.commit()
            return {"message": f"quote {quote.quote} successfully updated"}
        else:
            return {"message": "Unauthorized to update this quote", "quote": None}, 403

    elif request.method == 'DELETE':
        username = request.authorization.username
        user = UserModel.query.filter_by(username=username).first()
        if quote.user_id == user.id:
            db.session.delete(quote)
            db.session.commit()
            return {"message": f"Quote {quote.quote} successfully deleted."}
        else:
            return {"message": "Unauthorized to delete this quote", "quote": None}, 403

@app.route('/')
def show_random_quote():
    """Show a random quote from the database."""
    count = db.session.query(func.count(QuoteModel.id)).scalar()
    if count == 0:
        # if no quotes in the database, render a message
        message = "No quotes found in the database."
        return render_template("homepage.html", message=message)

    # get a random quote from the database
    random_id = random.randint(1, count)
    quote = QuoteModel.query.get(random_id)

    return render_template("homepage.html", quote=quote)

app.add_url_rule("/", endpoint="homepage", view_func=show_random_quote)


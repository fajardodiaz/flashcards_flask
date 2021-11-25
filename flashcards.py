from flask import Flask, render_template, abort, jsonify, request,redirect,url_for
from model import db, save_db

app = Flask(__name__)


#Main view - Welcome Page
@app.route('/')
def index():
    return render_template('welcome.html',message="This is a simple example",name="Friend", cards=db)


#Show only selected card
@app.route('/card/<int:card_id>')
def cards_view(card_id):
    try:
        card = db[card_id]
        return render_template("card.html",
        card=card,
        card_id=card_id,
        max_card_id=len(db)-1)
    except IndexError:
        abort(404)


#Show all cards
@app.route('/cards')
def cards():
    return render_template('cards.html',cards=db)


#show specific card in JSON (REST API)
@app.route('/api/card/<int:card_id>')
def api_card_detail(card_id):
    try:
        return db[card_id]
    except IndexError:
        return abort(404)


#show all cards in JSON (REST API)
@app.route('/api/cards')
def api_card_list():
    return jsonify(db)


# add cards
@app.route('/add_card',methods=["GET","POST"])
def add_card():
    if request.method == "POST":
        card = {"question":request.form["question"],"answer":request.form["answer"]}
        db.append(card)
        save_db()
        return redirect(url_for('cards'))

    return render_template('add_card.html')


# delete card
@app.route('/delete_card/<int:card_id>',methods=["GET","POST"])
def delete_card(card_id):
    try:
        if request.method == 'POST':
            del db[card_id]
            save_db()
            return redirect(url_for('cards'))
        return render_template('remove_card.html',card= db[card_id],card_id=card_id)
    except IndexError:
        abort(404)


# This function execute before a request
@app.before_request
def before_request():
    print("Before the request")


# This function execute after a request
@app.after_request
def after_request(response):
    print("After the request")
    return response


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, session, redirect,request, abort,jsonify
from app import create_app, setup_database

app = Flask(__name__)


def add_vue_routes(app):

    # function says default path is home
    @app.route('/', defaults={'path': ''})

    # function allows vue router to designate the 
    # content and just renders index.html no matter what 
    # path is used.
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template("index.html")

    # Clears cache for hot-reloading
    @app.after_request
    def add_header(req):
        req.headers["Cache-Control"] = "no-cache"
        return req
    
app = create_app()
add_vue_routes(app)
setup_database(app)

# Creates the app, database and all the routes
if __name__ == "__main__":
    app.run(debug=True)



# @app.route('/', methods=['GET'])
# def render_app():
#     has_shant_pooped = update_status()
#     if has_shant_pooped == True:
#         return render_template('index.html', message='Yes', last_poop_date=last_poop_date(), poop_message=poop_message(), poop_rating=poop_rating())
#     return render_template('index.html', message="No", last_poop_date=last_poop_date(), poop_message=poop_message(), poop_rating=poop_rating())


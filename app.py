from flask import Flask, request, render_template, session, make_response, jsonify
import jwt
import datetime
from functools import wraps
import json

from jwt.exceptions import ExpiredSignatureError, DecodeError

from src.pipeline.predict_pipeline import CustomData
from src.pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__)
app.config['SECRET_KEY'] = "3d2a877fc3074ec59014b8ad8b912143"

## functions
# storinng user credentials
def store_credentials(username, password, token):
    try:
        credentials = {'username': username, 'password': password, 'token': token}
        with open('templates/credentials.json', 'a') as file:
            json.dump(credentials, file)
            file.write('\n')  # Add a newline to separate entries
        print("Credentials stored successfully.")
    except Exception as e:
        print("An error occurred:", e)

def check_username(username):
    try:
        with open('templates/credentials.json', 'r') as file:
            for line in file:
                data = json.loads(line.strip())
                if data.get('username') == username:
                    return data
        return None  # Return None if username is not found
    except Exception as e:
        print("An error occurred:", e)
        return None
    

## routes for app 
@app.route("/")
def index():
    return render_template('index.html')
    
# admin page
@app.route("/get_credentials", methods=['GET'])
def get_credentials():
    try:
        with open('templates/credentials.json', 'r') as file:
            json_text = file.read()
            return json_text
            
    except:
        pass
    

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password != "admin":
            session["logged_in"] = True

            jwt_payload = {
                'user':request.form.get('username'),
                'exp': datetime.datetime.now() + datetime.timedelta(seconds=120)
            }
            token = jwt.encode(
                jwt_payload,
                app.config['SECRET_KEY']
            )
            
            # storing user credentials in json 
            try:
                # check if username is already there
                if check_username(username) == None:
                    store_credentials(username, password, token)
            except:
                return "couldn't save credentials"

            return jsonify({ 'token': token })
        
        else:
            return make_response("Unable to Verify User", 403)
        
    else:
        return render_template("login.html")

#
# write other function for authorization
#
def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        # You can use the JWT errors in exception
        # except ExpiredSignatureError:
        #     return "Token has expired", 401
        # except DecodeError:
        #     return 'Invalid token. Please log in again.', 401
        return func(*args, **kwargs)
    return decorated

# public and auth

@app.route('/auth')
@token_required
def auth():
    print('JWT is verified. Welcome to your dashboard !')
    return render_template("model.html")

@app.route('/public')
def public():
    return make_response('For Public. Go to /auth and verify your token', 200)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/predictdata", methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('model.html')
    else:
        df = CustomData(
            gender                      = request.form.get("gender"),
            race_ethnicity              = request.form.get("race_ethnicity"),
            parental_level_of_education = request.form.get("parental_level_of_education"),
            lunch                       = request.form.get("lunch"),
            test_preparation_course     = request.form.get("test_preparation_course"),
            reading_score               = float(request.form.get("reading_score")),
            writing_score               = float(request.form.get("writing_score"))
        )
        pred_df = df.get_data_as_dataframe()
        
        pred_pipeline = PredictionPipeline()
        res = pred_pipeline.predict(features=pred_df)

        return render_template('model.html', res=res[0])


# main function here
if __name__=="__main__":
    app.run()

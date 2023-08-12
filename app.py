from flask import Flask, request, render_template, make_response, jsonify
import datetime
import json
import requests

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from src.pipeline.predict_pipeline import CustomData
from src.pipeline.predict_pipeline import PredictionPipeline

import warnings
# Supress UserWarnings
warnings.filterwarnings("ignore", category=UserWarning)
# Restore warning behavior
# warnings.filterwarnings("default", category=UserWarning)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "3d2a877fc3074ec59014b8ad8b912143"

# creating jwt manager and giving app into it
jwt = JWTManager(app)

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
    except Exception as e:
        return jsonify({"Error":e })
    

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin":
            access_token = create_access_token(identity=username)
            # saving user credentials
            try:
                store_credentials(username, password, access_token)
            except Exception as e:
                return jsonify({"Error":e })
            
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            # response = requests.get("localhost:5000/auth", headers=headers)
            print(jsonify(headers))
            
            return jsonify({"token ": access_token})
        
        else:
            return make_response("unauthorized", 403)
    else:
        return render_template("login.html")

# public and auth

@app.route('/auth', methods=['GET', 'POST'])
@jwt_required()
def auth():
    print('JWT is verified. Welcome to your dashboard !')
    # curr_user = get_jwt_identity()
    # return jsonify(logged_in_as=curr_user), 200
    return render_template("model.html")

@app.route('/public')
# @jwt_required() #token req
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
    app.run(debug=True)

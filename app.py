from flask import Flask, request, render_template, make_response, jsonify, redirect, session, Blueprint
from bson import ObjectId
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

from src.pipeline.predict_pipeline import CustomData
from src.pipeline.predict_pipeline import PredictionPipeline

# creating blueprint
main = Blueprint('main', __name__)
api = Blueprint('api', __name__)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET")
app.config['MONGO_URI'] = os.getenv("MONGO_URI")
client = MongoClient(app.config['MONGO_URI'])

# Replace with your preferred database name
db = client.get_database('Profile')  
# Define a collection name(it can write by own also)
user_collection = db['users']
# Profile -> users  

# Configure logging
LOG_FILE =  f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=False)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# removing duplicates
logging.info("Preparing to remove duplicates from database")
pipeline = [{
        '$group': {
            '_id': '$username',  # Group by the field you want to de-duplicate
            'duplicates': {'$addToSet': '$_id'},  # Collect _ids of duplicates
            'count': {'$sum': 1}  # Count occurrences of each group
        }},
    {
        '$match': {
            'count': {'$gt': 1}  # Filter groups with more than 1 occurrence (duplicates)
        }}]
def rem_dups():
    duplicate_groups = list(user_collection.aggregate(pipeline))
    for group in duplicate_groups:
        # Keep the first occurrence, remove duplicates
        keep_id = group['duplicates'][0]
        remove_ids = group['duplicates'][1:]
        user_collection.delete_many({'_id': {'$in': remove_ids}})
    logging.info("Duplicates removed successfully")
FLAG = True
if FLAG:
    rem_dups()
    FLAG=False
    logging.info("FLAG value toggled")



# adding sessions for protected routes
@main.route('/check')
def check_session():
    logging.info("dashboard page is accessed")
    if 'user_id' in session:
        user_id = session['user_id']
        # Retrieve user data based on user_id
        user = user_collection.find_one({'_id': ObjectId(user_id)})
        if user:
            return f"Welcome, {user['username']}!"
    return "Unauthorized. Please login first."

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# define routes
@main.route('/')
def index():
    logging.info("Index page is accessed")
    return render_template("index.html")


# retrieve all users 
@api.route('/user_list')
def user_list():
    logging.info("users list is accessed")
    users = user_collection.find()  # Retrieve all documents from the collection
    return render_template('user_list.html', users=users)


# search users by objectID
@api.route('/get_username/<user_id>')
def user_details(user_id):
    logging.info("searched for user using ObjectID")
    user = user_collection.find_one({'_id': ObjectId(user_id)})  # Find user by ID
    if user:
        return render_template('user_details.html', user=user)
    else:
        return "User not found."
    

@api.route('/new_users')
def latest_users():
    logging.info("checked latest users entry")
    latest_users = user_collection.find().sort('created_at', DESCENDING).limit(5)
    return render_template('latest_users.html', users=latest_users)


# get ObjectID from username
@api.route('/get_userid/<username>')
def get_user_id(username):
    logging.info("fetched ObjectID using username")
    user = user_collection.find_one({'username': username})
    if user:
        user_id = str(user['_id'])  # Convert ObjectId to string
        return f"The ObjectId of user '{username}' is: {user_id}"
    else:
        return "User not found."

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    logging.info("Landed on signup page")
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        timestamp = datetime.now()

        # Check if the username already exists in the users collection
        if user_collection.find_one({'username': username}):
            return "Username already taken."

        user_data = {
            'email': email,
            'username': username,
            'password': password,  # In a real application, you should hash the password
            'Joined': timestamp
        }
        user_collection.insert_one(user_data)
        logging.info("Signup Successful")
        return "User signed up successfully."

    return render_template('signup.html')



@main.route("/login", methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = user_collection.find_one({'username': username, 'password': password})
        if user:
            # Set session for logged-in user
            session['user_id'] = str(user['_id'])
            logging.info("Login Successful")
            return redirect("auth")
        else:
            return "Invalid credentials."

# public and auth

@main.route('/auth', methods=['GET', 'POST'])
def auth():
    print('Welcome to the app!')
    return render_template("model.html")
    

@main.route('/public')
def public():
    return make_response('For Public. Go to /auth and verify your token', 200)


@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/predictdata", methods=['GET', 'POST'])
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



# Register the blueprints
app.register_blueprint(main)
app.register_blueprint(api, url_prefix='/api')

# main function here
if __name__=="__main__":
    app.run(debug=True)

from flask import Flask, request, render_template

from src.pipeline.predict_pipeline import CustomData
from src.pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__)

# routes for app
@app.route("/")
def index():
    return render_template('index.html')


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
    app.run(debug=False)

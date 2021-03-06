import os
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, make_response, jsonify, request
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def get_model():
    iris = datasets.load_iris()
    model = RandomForestClassifier(n_estimators=1000).fit(iris.data, iris.target)
    labels = list(iris.target_names)
    return model, labels


MODEL, LABELS = get_model()


@app.route('/')
def index():
    return make_response(open(os.path.join(DIR, 'index.html')).read())


@app.route('/api/predict')
def predict():
    def getter(label):
        return float(request.args.get(label, 0))
    try:
        features = map(getter, ['sepalLength', 'sepalWidth', 'petalLength', 'petalWidth'])
        probs = MODEL.predict_proba(features)[0]
    except ValueError:
        probs = (1. / len(LABELS) for _ in LABELS)

    val = {"data": [{"label": label, "prob": prob} for label, prob in zip(LABELS, probs)]}
    return jsonify(val)

#Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

app.secret_key = 'super_secret_key'

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

#if __name__ == '__main__':
#    app.run()

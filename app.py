from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
from scripts.qa import generate_response

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")
# CORS(app)

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = generate_response(text)
    message = {"answer":response}
    return jsonify(message)

if __name__ =="__main__":
    app.run(host='127.0.0.1', port=5001,debug=True)
    #app.run(debug=True)


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
    expl, sim, max_sim = None, None, None
    counter = 1
    text = request.get_json().get("message")
    if text.lower() == 'more info':
        for i in range(counter,len(sim)):
            ansr = expl[sim.index(max_sim[i])]
            counter +=1
    else:
        expl, sim, max_sim = generate_response(text)
        ansr = expl[sim.index(max_sim[0])]

    response = ansr + "\n\nIf you want to know more, type \"More info\"."
    message = {"answer": response}
    return jsonify(message)

if __name__ =="__main__":
    app.run(host='127.0.0.1', port=5001,debug=True)
    #app.run(debug=True)


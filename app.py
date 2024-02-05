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
    global sim, expl, max_sim

    global counter
    text = request.get_json().get("message")
    if text.lower() == 'more info' and counter < len(sim):
        ansr = expl[sim.index(max_sim[counter])]
        counter += 1
    elif text.lower() != 'more info':
        counter = 1
        expl, sim, max_sim = generate_response(text)
        if expl:
            ansr = expl[sim.index(max_sim[0])]
        else:
            ansr = "Sorry, I don't know about that!"
    else:
        ansr = "That's all the information we've got. Sorry!"

    ansr += "\n   If you want to know more, type \"More info\"."
    message = {"answer": ansr}
    return jsonify(message)

if __name__ =="__main__":
    app.run(host='127.0.0.1', port=5001,debug=True)
    #app.run(debug=True)


from flask import Flask, request, jsonify
from model import EmbeddingModel


model = None

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/train", methods=['POST'])
def train():
    global model
    data_reset = request.get_json()
    X = [data_reset['user_history'], data_reset['item_history']]
    y = data_reset['rating_history']
    nb_users, nb_items = data_reset['nb_users'], data_reset['nb_items']

    model = EmbeddingModel(nb_users, nb_items, embedding_size=30)
    model.fit(X, y, verbose=True)

    return jsonify({'info':'successful'})



@app.route("/predict", methods=['GET', 'POST'])
def predict():
    global model
    user = int(request.args.get('user'))
    item = int(request.args.get('item'))
    print(user, item)
    next_X = [[user], [item]]

    prediction = model.predict(next_X)

    return jsonify([{'user':user, 'item':item, 'rating':prediction}])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import config
import os
from chat import get_chat_response

# create and configure the app
app = Flask(__name__)
CORS(app)

# default to dev config
if (os.getenv('BACKEND_ENV') or 'dev') == 'dev':
    app.config.from_object(config.DevelopmentConfig)
else:
    app.config.from_object(config.ProductionConfig)

# TODO: add error handling


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    print(request.headers)
    # TODO: add memory to chatbot
    # TODO: add moderation layer
    # TODO: add fact checker
    response = get_chat_response(data['query'])
    return make_response(jsonify({"message": response}), 200)


if __name__ == '__main__':
    app.run()

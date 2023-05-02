from flask import Flask

app = Flask(__name__)


@app.route('/search')
def search():
    """First find most relevant chunks, then pass to gpt as context"""
    pass


def get_most_relevant_chunks(prompt):

    pass

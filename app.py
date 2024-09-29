from flask import Flask, request, jsonify
from parse import extract_content, chunk_text, save_to_chroma

app = Flask(__name__)

@app.route('/test')
def test():
    text = extract_content("public/cricket.pdf")
    chunks = chunk_text(text)
    save_to_chroma(chunks)
    return jsonify({"message": "success"})


@app.route('/api/get_learning_path', methods=['POST'])
def get_learning_path():
    data = request.get_json()
    print(data)

@app.route('/api/ask_doubt', methods=['POST'])
def ask_doubts():
    data = request.get_json()
    print(data)


if __name__ == '__main__':
    app.run(port=5000)
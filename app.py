import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from parse import extract_content, chunk_text, save_to_chroma
from summarise_and_quiz import get_summary_and_quiz
from doubt import answer_doubt
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()


@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'pdf' not in request.files:
            return jsonify({"error": "No file part"})
        pdf = request.files['pdf']
        pdf.save("public/file.pdf")
    
        return jsonify({
            "message": "File uploaded successfully",
            "success": True
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "error": str(e)
        })


@app.route('/api/get_learning_path', methods=['POST'])
def get_learning_path():
    try:
        print(request.get_json())
        difficulty_level = 'easy'
        document_text = extract_content("public/file.pdf")
        chunks = chunk_text(document_text)
        save_to_chroma(chunks)

        summary, quiz = get_summary_and_quiz(document_text, difficulty_level)
        return jsonify({
            "summary": summary, "quiz": quiz
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "error": str(e)
        })

@app.route('/api/ask_doubt', methods=['POST'])
def ask_doubts():
    data = request.get_json()
    print(data)
    doubt = data['doubt']
    response = answer_doubt(doubt)

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(port=5000)
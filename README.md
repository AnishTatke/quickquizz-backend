# Flask Backend

This is a basic Flask backend project.

## Requirements

- Python 3.x
- Flask

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install Flask
    ```

## Running the Application

1. Set the FLASK_APP environment variable:
    ```sh
    export FLASK_APP=app.py  # On Windows use `set FLASK_APP=app.py`
    ```

2. Run the Flask application:
    ```sh
    flask run
    ```

3. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Project Structure

```
/your-repo
│
├── app.py
├── requirements.txt
├── venv/
└── README.md
```

## Example Code

`app.py`:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```

## License

This project is licensed under the MIT License.
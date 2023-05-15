from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/settings/', methods=['POST'])
def settings():
    key = request.headers.get('key')
    if key != 'VALIDATION_KEY':
        return 'Invalid key', 401
    settings = request.get_json()
    with open('settings.conf', 'w') as f:
        json.dump(settings, f)
    return 'Settings saved', 200

if __name__ == '__main__':
    app.run(port=8080)

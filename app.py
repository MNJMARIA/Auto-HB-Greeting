from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/send_telegram', methods=['POST'])
def send_telegram():
    # Ваш код для надсилання повідомлень у Telegram
    return 'Telegram message sent!'

if __name__ == '__main__':
    app.run(debug=True)

#from flask import Flask

#app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello, World!'

#@app.route('/send_telegram', methods=['POST'])
#def send_telegram():
#    # Ваш код для надсилання повідомлень у Telegram
#    return 'Telegram message sent!'

#if __name__ == '__main__':
#    app.run(debug=True)



from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio

app = Flask(__name__)

api_id = '17860937'
api_hash = '6bdbb8eae683414b8d13798b2b37640b'
phone = '+380936707972'  # Ваш номер телефону

client = TelegramClient('birthday_greetings_session', api_id, api_hash)

async def send_message(phone_number, message):
    await client.start(phone)
    await client.send_message(phone_number, message)
    await client.disconnect()

@app.route('/')
def hello_world():
    return 'Hellooo, World!'


@app.route('/send_greeting', methods=['POST'])
def send_greeting():
    data = request.json
    phone_number = data.get('phone_number')
    message = data.get('message')

    if not phone_number or not message:
        return jsonify({"status": "error", "message": "Phone number or message is missing"}), 400

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_message(phone_number, message))
    except Exception as e:
        app.logger.error(f"Error sending message: {e}")
        return jsonify({"status": "error", "message": f"Failed to send message: {str(e)}"}), 500

    return jsonify({"status": "success", "message": f"Greeting sent to {phone_number}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


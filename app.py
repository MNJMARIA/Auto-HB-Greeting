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
import threading

app = Flask(__name__)

# Telegram credentials
api_id = '17860937'
api_hash = '6bdbb8eae683414b8d13798b2b37640b'
phone = '+380936707972'  # Your phone number


client = TelegramClient('birthday_greetings_session', api_id, api_hash)

async def send_message(phone_number, message):
    async with client:
        await client.send_message(phone_number, message)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/send_message', methods=['POST'])
def send_telegram_message():
    data = request.json
    print("Received data:", data)  # Logging for debugging

    phone_number = data.get('phone_number')
    message = data.get('message')

    if not phone_number or not message:
        return jsonify({'status': 'error', 'message': 'Missing phone_number or message'}), 400

    try:
        # Run the async function in a separate thread to avoid blocking the Flask server
        loop = asyncio.new_event_loop()
        threading.Thread(target=lambda: loop.run_until_complete(send_message(phone_number, message))).start()
        return jsonify({'status': 'success', 'message': f'Message sent to {phone_number}'})
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

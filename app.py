from quart import Quart, request, jsonify
from telethon import TelegramClient

app = Quart(__name__)

api_id = '17860937'
api_hash = '6bdbb8eae683414b8d13798b2b37640b'
phone = '+380936707972'  # Ваш номер телефону

client = TelegramClient('birthday_greetings_session', api_id, api_hash)

async def send_message(phone_number, message):
    async with client:
        await client.send_message(phone_number, message)

@app.route('/')
async def hello_world():
    return 'Hellooo, Wooorld!'

@app.route('/send_greeting', methods=['POST'])
async def send_greeting():
    data = await request.get_json()
    phone_number = data.get('phone_number')
    message = data.get('message')
    
    if not phone_number or not message:
        return jsonify({"status": "error", "message": "Phone number or message is missing"}), 400

    try:
        await send_message(phone_number, message)
        return jsonify({"status": "success", "message": f"Greeting sent to {phone_number}"})
    except Exception as e:
        app.logger.error(f"Error sending message: {e}")
        return jsonify({"status": "error", "message": f"Failed to send message: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


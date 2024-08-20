from quart import Quart, request, jsonify
from telethon import TelegramClient

app = Quart(__name__)

api_id = '17860937'
api_hash = '6bdbb8eae683414b8d13798b2b37640b'
phone = '+380936707972'  # Ваш номер телефону

client = TelegramClient('birthday_greetings_session', api_id, api_hash)

async def send_message(phone_number, message):
    try:
        print("6.1 Створюємо новий сеанс клієнта")
        async with client:
            print("6.2 Сеанс клієнта відкритий, надсилаємо повідомлення")
            await client.send_message(phone_number, message)
            print("6.3 Повідомлення надіслано успішно")
    except Exception as e:
        print(f"6.4 Виникла помилка в send_message: {e}")
        raise e


@app.route('/')
async def hello_world():
    return 'Hellooo, Wooorld!'

@app.route('/send_greeting', methods=['POST'])
async def send_greeting():
    print("1. Отримано запит на /send_greeting")
    
    data = await request.get_json()
    print("2. Отримано дані:", data)
    
    phone_number = data.get('phone_number')
    message = data.get('message')
    print(f"3. Витягнуто номер телефону: {phone_number}, повідомлення: {message}")
    
    if not phone_number or not message:
        print("4. Відсутній номер телефону або повідомлення")
        return jsonify({"status": "error", "message": "Phone number or message is missing"}), 400

    try:
        print("5. Початок надсилання повідомлення")
        await send_message(phone_number, message)
        print("6. Повідомлення успішно надіслано")
        return jsonify({"status": "success", "message": f"Greeting sent to {phone_number}"})
    except Exception as e:
        print(f"7. Виникла помилка при надсиланні повідомлення: {e}")
        app.logger.error(f"Error sending message: {e}")
        return jsonify({"status": "error", "message": f"Failed to send message: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


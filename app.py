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
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

api_id = '17860937'  # Ваш API ID
api_hash = '6bdbb8eae683414b8d13798b2b37640b'
phone = '+380936707972'  # Ваш номер телефону

client = TelegramClient('birthday_greetings_session', api_id, api_hash)

# Створюємо один цикл подій, який будемо використовувати для асинхронних завдань
loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor(max_workers=1)

async def send_message(phone_number, message):
    async with client:
        try:
            user = await client.get_entity(phone_number)  # Отримуємо користувача за номером телефону
            await client.send_message(user, message)
            return 'Message sent!'
        except Exception as e:
            return f"Error: {e}"

def run_async(coroutine):
    return loop.run_until_complete(coroutine)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/send_message', methods=['POST'])
def send_telegram_message():
    data = request.json
    phone_number = data.get('phone_number')
    message = data.get('message')
    
    if not phone_number or not message:
        return jsonify({'status': 'error', 'message': 'Missing phone_number or message'}), 400
    
    try:
        # Запускаємо асинхронну функцію в ThreadPoolExecutor
        future = executor.submit(run_async, send_message(phone_number, message))
        response_message = future.result()  # Чекаємо завершення асинхронної функції
        return jsonify({'status': 'success', 'message': response_message})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


from aiogram import Bot, Dispatcher, types, executor
import requests
from geopy.distance import geodesic

token = '6352717098:AAHiRxkzT8JTCnhCDlpObVswDkZYLv65D7o'
bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['id'])
async def id_cmd(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f'ID вашего чата: {chat_id}')

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chatid = message.chat.id

    await bot.send_message(chatid, "Сверка айпи Блек Раша мужская игра онлайн - Бот для проверки iP.\n\nНапиши и ознакомся пока с - /help")

@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    chatid = message.chat.id
    await bot.send_message(chatid, text="/ip [ip]- Проверяет 1 iP\n/ips [ip1] [ip2] - Проверяет 2 iP")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def process_text_message(message: types.Message):

    ip_addresses = message.text.split()

    if len(ip_addresses) == 1:

        ip_info = get_ip_info(ip_addresses[0])
        await message.reply(f'<b>IP -</b> {ip_addresses[0]}:\n{format_ip_info(ip_info)}', parse_mode=types.ParseMode.HTML)
    elif len(ip_addresses) == 2:

        ip_info1 = get_ip_info(ip_addresses[0])
        ip_info2 = get_ip_info(ip_addresses[1])


        coord1 = (ip_info1['lat'], ip_info1['lon'])
        coord2 = (ip_info2['lat'], ip_info2['lon'])


        distance_km = geodesic(coord1, coord2).kilometers

        response_text = (
            f"<b>IP 1 -</b> {ip_addresses[0]}\n{format_ip_info(ip_info1)}\n\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
            f"<b>IP 2 -</b> {ip_addresses[1]}:\n{format_ip_info(ip_info2)}\n\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
            f"Расстояние между координатами: <b>{distance_km:.2f} км</b>"
        )

        await message.reply(response_text, parse_mode=types.ParseMode.HTML)
    else:
        await message.reply('Пожалуйста, введите один или два IP-адреса в текстовом формате.')

def get_ip_info(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}?lang=ru&fields=215007')
    data = response.json()
    return data

def format_ip_info(data):
    if data['status'] == 'fail':
        return ("Один из введенных IP недействительный, проверьте написание IP адерсов.")
    else:
        return (
        f"Страна: {data['country']}\n"
        f"Город: {data['city']}\n"
        f"Регион: {data['regionName']}\n\n"
        "<b>Информация о провайдере:</b>\n\n"
        f"Провайдер: {data['isp']}\n"
        f"Доп. информация о провайдере: {data['org']}\n"
        f"Мобильный интернет: {data['mobile']}\n"
        f"Прокси/VPN: {data['proxy']}"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
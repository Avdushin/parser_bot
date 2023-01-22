from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

# from keyboards.inline.callback_datas import parse_callback
from keyboards.inline.choice_buttons import parse_service
from loader import dp, bot

from bs4 import BeautifulSoup as bs
import requests, logging, re


@dp.message_handler(Command("items"))
async def show_items(message: Message):
    await message.answer(text="Выберете сервис",
                         reply_markup=parse_service)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "rbc"
@dp.callback_query_handler(text_contains="rbc")
async def buying_pear(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=60)

    callback_data = call.data

    # Отобразим что у нас лежит в callback_data
    # logging.info(f"callback_data='{callback_data}'")
    logging.info(f"{callback_data=}")

    # mask
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    url = 'https://www.rbc.ru/'

    response = requests.get(url, headers=headers)

    soup = bs(response.text, "lxml")
    all_news_part = soup.find_all("div", class_="main__feed js-main-reload-item")

    # print(f"DATA_RBC: \n{all_news_part}\n")

    news_dict = []
    for news in all_news_part:
        # извлекаем дату
        match = re.search(r'data-modif-date=[^.]+\+0300">', str(news))
        date_dirt = match[0]
        date = date_dirt[17:-7]
        # извлекаем url
        url = news.a['data-vr-contentbox-url']
        # извлекаем новость
        content = news.find('span', class_="main__feed__title-wrap").get_text(strip=True)

        news_dict.append({
            'date': date,
            'url': url,
            'content': content,
        })

    for item in news_dict:
        await call.message.answer(
            f'\n\nВремя: {item["date"]}\nНовость: {item["content"]}\nКонтент: {item["url"]}\n\n\n**********************\n')

# Vesta parser
@dp.callback_query_handler(text_contains="vesta")
async def buying_pear(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=60)

    callback_data = call.data

    # Отобразим что у нас лежит в callback_data
    # logging.info(f"callback_data='{callback_data}'")
    logging.info(f"{callback_data=}")

    # mask
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    url = 'https://vestaunion.ru/?page_id=384'

    response = requests.get(url, headers=headers)

    soup = bs(response.text, "lxml")
    all_news_part = soup.find_all("div", class_="pt-cv-ifield")
    # Parse test
    # print(f"ALL_NEWS_PART: \n{all_news_part}\n")
    news_dict = []
    for news in all_news_part:
        # извлекаем дату
        date = news.find('span', class_="entry-date").get_text(strip=True)
        # извлекаем url
        url = news.a['href']
        # извлекаем новость
        content = news.find('h4', class_="pt-cv-title").get_text(strip=True)

        news_dict.append({
            'date': date,
            'url': url,
            'content': content,
        })

    for item in news_dict:
        await call.message.answer(
            f'\n\n<b>Время:</b> {item["date"]}\n<b>Новость:</b> {item["content"]}\n<b>Контент:</b> {item["url"]}\n\n\n**********************\n')


@dp.callback_query_handler(text="cancel")
async def cancel(call: CallbackQuery):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы отменили выбор сервисов!", show_alert=True)

    # Вариант 1 - Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup=None)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import parse_callback

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")

###############
# Markup
parse_service = InlineKeyboardMarkup(row_width=2)

# Buttons initialization
parse_rbc = InlineKeyboardButton(
    text="rbc", callback_data=parse_callback.new(service="rbc"))
parse_vesta = InlineKeyboardButton(
    text="vesta", callback_data=parse_callback.new(service="vesta"))

# Buttons append
parse_service.insert(parse_rbc)
parse_service.insert(parse_vesta)
parse_service.insert(cancel_button)
###############

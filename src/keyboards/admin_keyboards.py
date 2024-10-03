from aiogram import Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

rt = Router()


async def admin_keyboard():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Администраторы 🔥",
                        callback_data="admins"
                    )
                ],
                # [
                #     InlineKeyboardButton(
                #         text="Старосты ✨",
                #         callback_data="headman"
                #     )
                # ],
                [
                    InlineKeyboardButton(
                        text="Показать плохих ребят 😈",
                        callback_data="banwords"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Настройки чата 🧰",
                        callback_data="chat"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Информация 📚",
                        callback_data="info"
                    )
                ]
            ]
        )


async def admins():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить администратора ✅",
                    callback_data="add_admin"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Удалить администратора ❎",
                    callback_data="del_admin"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад ↩",
                    callback_data="back"
                )
            ]
        ]
    )


async def headman():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить старосту ✅",
                    callback_data="add_headman"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Удалить старосту ❎",
                    callback_data="del_headman"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад ↩",
                    callback_data="back"
                )
            ]
        ]
    )


async def chat_settings():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Включить чат ✅",
                    callback_data="chat_on"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отключить чат ❎",
                    callback_data="chat_off"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад ↩",
                    callback_data="back"
                )
            ]
        ]
    )


async def chat_on():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Включить чат ✅",
                    callback_data="chat_on"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад ↩",
                    callback_data="back"
                )
            ]
        ]
    )


async def chat_off():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Отключить чат ✅",
                    callback_data="chat_off"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад ↩",
                    callback_data="back"
                )
            ]
        ]
    )


async def back():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад ↩",
                    callback_data="back"
                )
            ]
        ]
    )
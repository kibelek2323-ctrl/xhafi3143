from __future__ import annotations

import asyncio
import logging
import os
from typing import Dict

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID", "0") or 0)
VOUCHER_URL = "https://www.g2a.com/paypal-gift-card-5-eur-by-rewarble-global-i10000339995019"

router = Router()
purchase_sessions: Dict[int, str] = {}


def kb(rows: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=rows)


def main_menu_kb() -> InlineKeyboardMarkup:
    return kb([
        [InlineKeyboardButton(text="Features", callback_data="features")],
        [InlineKeyboardButton(text="Payment Methods", callback_data="payments")],
        [InlineKeyboardButton(text="FAQ", callback_data="faq")],
        [InlineKeyboardButton(text="Changelog", callback_data="changelog")],
        [InlineKeyboardButton(text="Status", callback_data="status")],
        [InlineKeyboardButton(text="Purchase License", callback_data="purchase")],
    ])


def back_kb() -> InlineKeyboardMarkup:
    return kb([[InlineKeyboardButton(text="Back", callback_data="home")]])


def purchase_kb() -> InlineKeyboardMarkup:
    return kb([
        [InlineKeyboardButton(text="1 Week - 5 EUR", callback_data="plan:1 Week - 5 EUR")],
        [InlineKeyboardButton(text="1 Month - 10 EUR", callback_data="plan:1 Month - 10 EUR")],
        [InlineKeyboardButton(text="Lifetime - 20 EUR", callback_data="plan:Lifetime - 20 EUR")],
        [InlineKeyboardButton(text="Back", callback_data="home")],
    ])


def platform_kb(plan: str) -> InlineKeyboardMarkup:
    return kb([
        [
            InlineKeyboardButton(text="Android", callback_data=f"platform:{plan}:Android"),
            InlineKeyboardButton(text="iOS", callback_data=f"platform:{plan}:iOS"),
        ],
        [InlineKeyboardButton(text="Back", callback_data="purchase")],
    ])


def voucher_kb(plan: str, platform: str) -> InlineKeyboardMarkup:
    return kb([
        [InlineKeyboardButton(text="Buy 5 EUR Revolut Voucher", url=VOUCHER_URL)],
        [InlineKeyboardButton(text="Back", callback_data=f"plan:{plan}")],
    ])


WELCOME = """<b>Welcome to Ultimate Stars Bot</b>

One of the best options available right now.
Running on v67.264 - kept up to date with every game patch.

Use the buttons below to get started.
"""

FEATURES = """<b>Features</b>

<b>Auto Dodge</b>
Reads incoming projectiles in real time and moves out of the way automatically. Fast enough to catch things human reaction cannot, and smooth enough that it looks completely natural.

<b>Aimbot</b>
Predicts enemy movement and keeps your aim locked on. No snapping, no jitter - looks like a real player, just does not miss.

<b>BSD Brawl Features</b>
Full BSD module pack - visual tweaks, map awareness overlays, and extra options that are not in any other mod.

<i>Updated every time the game patches so nothing breaks on you.</i>
"""

PAYMENTS = """<b>Payment Methods</b>

All payments go through Rewarble Revolut vouchers on Eneba.
Eneba supports a wide range of payment options:

- Credit / Debit Card
- PayPal
- Cryptocurrency
- Paysafecard
- Venmo
- iDEAL
- Sofort
- and more depending on your region.

You buy the voucher on Eneba, send the key here - that is it.

<i>No account needed, no personal info stored.</i>
"""

FAQ = """<b>FAQ</b>

<b>Is it safe to use?</b>
Yes. Ultimate Stars runs externally and does not modify any game files directly. Detection risk is kept as low as possible and we monitor things closely after every update.

<b>How long does delivery take?</b>
Usually within a few minutes after your key is verified. If it takes longer, sit tight - it will come through.

<b>Does it work in all game modes?</b>
Yes, all features work across every game mode.

<b>Will my account get banned?</b>
No bans have been reported from using Ultimate Stars. That said, no mod is ever 100% risk-free - use it sensibly.

<b>I paid but have not received anything.</b>
Make sure you sent the gift card key in the bot chat. If you did and it has been more than 10 minutes, support will follow up shortly.

<b>Does it work on iOS?</b>
Yes, iOS is supported. The setup process is slightly different - after purchasing you will be guided through it.
"""

CHANGELOG = """<b>Changelog</b>

<b>v67.264 - May 11, 2025</b>
- Auto Dodge: improved projectile prediction at close range, reduced occasional stuttering on fast attacks
- Auto Dodge: fixed an edge case where dodge would trigger late against certain Brawlers
- Aimbot: tightened tracking consistency, aim now holds better through target movement changes
- Aimbot: minor smoothing improvements to make movement look more natural at high speeds
- Authentication: resolved intermittent login failures some users were experiencing on startup
- Authentication: improved session handling to prevent unexpected disconnects mid-game
- General stability improvements

<i>Previous versions available on the Discord server.</i>
"""

STATUS = """<b>Ultimate Stars - Status</b>

Everything is running fine.
The service is up to date and fully operational.
"""

PURCHASE = """<b>Purchase a License</b>

All plans include every feature - no restrictions.

<b>1 Week</b>  - 5 EUR
<b>1 Month</b> - 10 EUR
<b>Lifetime</b> - 20 EUR

<i>Payment is handled through Rewarble Revolut vouchers.</i>
"""


@router.message(CommandStart())
async def start(message: Message) -> None:
    purchase_sessions.pop(message.from_user.id, None)
    await message.answer(WELCOME, reply_markup=main_menu_kb())


@router.callback_query(F.data == "home")
async def home(call: CallbackQuery) -> None:
    purchase_sessions.pop(call.from_user.id, None)
    await call.message.edit_text(WELCOME, reply_markup=main_menu_kb())
    await call.answer()


@router.callback_query(F.data == "features")
async def features(call: CallbackQuery) -> None:
    await call.message.edit_text(FEATURES, reply_markup=back_kb())
    await call.answer()


@router.callback_query(F.data == "payments")
async def payments(call: CallbackQuery) -> None:
    await call.message.edit_text(PAYMENTS, reply_markup=back_kb())
    await call.answer()


@router.callback_query(F.data == "faq")
async def faq(call: CallbackQuery) -> None:
    await call.message.edit_text(FAQ, reply_markup=back_kb())
    await call.answer()


@router.callback_query(F.data == "changelog")
async def changelog(call: CallbackQuery) -> None:
    await call.message.edit_text(CHANGELOG, reply_markup=back_kb())
    await call.answer()


@router.callback_query(F.data == "status")
async def status(call: CallbackQuery) -> None:
    await call.message.edit_text(STATUS, reply_markup=back_kb())
    await call.answer()


@router.callback_query(F.data == "purchase")
async def purchase(call: CallbackQuery) -> None:
    await call.message.edit_text(PURCHASE, reply_markup=purchase_kb())
    await call.answer()


@router.callback_query(F.data.startswith("plan:"))
async def choose_plan(call: CallbackQuery) -> None:
    plan = call.data.split(":", 1)[1]
    await call.message.edit_text(
        f"<b>{plan}</b>\n\nBefore we continue - are you on iOS or Android?",
        reply_markup=platform_kb(plan),
    )
    await call.answer()


@router.callback_query(F.data.startswith("platform:"))
async def choose_platform(call: CallbackQuery) -> None:
    _, plan, platform = call.data.split(":", 2)
    purchase_sessions[call.from_user.id] = f"{plan} ({platform})"

    text = f"""<b>{plan} ({platform})</b>

1. Hit the button below and grab the <b>5 EUR Revolut voucher</b>.

2. Eneba takes card, PayPal, crypto, Paysafecard, Venmo and more.

3. Once you have it, come back here and send the key as a message in this chat.

4. Once the key is verified, the file will be sent to you automatically.
"""
    await call.message.edit_text(text, reply_markup=voucher_kb(plan, platform))
    await call.message.answer(
        f"<b>{plan} ({platform})</b>\n\n"
        "Send the gift card key in this chat and it gets logged straight away.\n\n"
        "<i>Paste it as a plain message, nothing else needed.</i>"
    )
    await call.answer()


@router.message(F.text)
async def catch_key(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    context = purchase_sessions.get(user_id)

    if not context:
        await message.answer("Use /start and choose a license first. Then paste your voucher key here.")
        return

    key_text = message.text.strip()

    await message.answer(
        "✅ Key received. It has been logged for verification.\n"
        "Please wait while support checks it."
    )

    if ADMIN_ID:
        user = message.from_user
        await bot.send_message(
            ADMIN_ID,
            "<b>New voucher key submitted</b>\n\n"
            f"<b>User:</b> {user.full_name} (@{user.username or 'no_username'})\n"
            f"<b>User ID:</b> <code>{user.id}</code>\n"
            f"<b>Plan:</b> {context}\n"
            f"<b>Key:</b> <code>{key_text}</code>",
        )


async def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE":
        raise RuntimeError("Set BOT_TOKEN in .env before starting the bot.")

    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

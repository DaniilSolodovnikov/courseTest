import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN
from services.currency_service import CurrencyService
from services.redis_service import RedisService
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
redis_service = RedisService()
currency_service = CurrencyService(redis_service)


async def on_startup(dp):
    await redis_service.connect()
    await currency_service.update_rates()


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I can help you with currency exchange rates.")


@dp.message_handler(commands=["rates"])
async def send_rates(message: types.Message):
    rates = await redis_service.get("*")
    if rates:
        response = "Current Exchange Rates:\n"
        for key, value in rates.items():
            response += f"{key}: {value}\n"
        await message.reply(response)
    else:
        await message.reply("Rates are not available at the moment.")


@dp.message_handler(commands=["exchange"])
async def exchange(message: types.Message):
    try:
        args = message.text.split()
        if len(args) == 4:
            from_currency, to_currency, amount = args[1], args[2], float(args[3])
            rate = await currency_service.get_rate(from_currency, to_currency)
            if rate:
                result = amount * rate
                await message.reply(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}")
            else:
                await message.reply("Invalid currency codes.")
        else:
            await message.reply("Please use the format: /exchange <from_currency> <to_currency> <amount>")
    except ValueError:
        await message.reply("Invalid amount.")
if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
import asyncio
import logging
from xml.etree import ElementTree as ET
import aiohttp

import config

# from .redis_service import RedisService


logger = logging.getLogger(__name__)


class CurrencyService:
    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service

        async def update_rates(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(config.CB_URL) as response:
                    if response.status == 200:
                        xml_data = await response.text()
                        root = ET.fromstring(xml_data)
                        for valute in root.findall(".//Valute"):
                            code = valute.find("CharCode").text
                            value = float(valute.find("Value").text.replace(",", "."))
                            await self.redis_service.set(code, value)
                            logger.info(f"Updated rate for {code}: {value}")
                    else:
                        logger.error(f"Error fetching data from {config.CB_URL}: {response.status}")

        async def get_rate(self, from_currency, to_currency):
            from_rate = await self.redis_service.get(from_currency)
            to_rate = await self.redis_service.get(to_currency)
            if from_rate and to_rate:
                return float(from_rate) / float(to_rate)
            else:
                return None
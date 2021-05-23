import asyncio
import aiohttp
from .exceptions import *


class TwoCaptcha:
    """
    2Captcha Captcha Class

    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        """
        2Captcha API Key
        """

    async def solve(self, public_key):
        """

        Solves the captcha With the Token

        """
        url = f'https://2captcha.com/in.php?key={self.api_key}&method=funcaptcha&publickey={public_key}' \
              f'&surl=https://roblox-api.arkoselabs.com&pageurl=https://www.roblox.com&json=1'
        async with aiohttp.ClientSession() as f:
            async with f.post(url) as aa:
                data = await aa.json()
            if data['request'] == "ERROR_ZERO_BALANCE":
                raise InsufficientCredit(
                    "Insufficient credit in the 2captcha account.")
            if data['request'] == "ERROR_NO_SLOT_AVAILABLE":
                raise NoAvailableWorkers(
                    "There are currently no available workers.")
            if data['request'] == "ERROR_WRONG_USER_KEY" or data['request'] == "ERROR_KEY_DOES_NOT_EXIST":
                raise InvalidAPIToken(
                    "The provided 2captcha api key was incorrect.")
            task_id = data['request']

            while True:
                await asyncio.sleep(5)
                async with f.post(f"https://2captcha.com/res.php?key={self.api_key}&id={task_id}&json=1&action=get") as lm:
                    data_json = await lm.json()
                if data_json['request'] != "CAPCHA_NOT_READY":
                    solution = data_json['request']
                    break
            return solution

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
            if data['request'] == "IP_BANNED":
                raise IpBanned(
                    "Your IP address is banned due to many frequent attempts to access the server using "
                    "wrong authorization keys. ")
            if data['request'] == "ERROR_IP_NOT_ALLOWED":
                raise IpNotAllowed(
                    "The request is sent from the IP that is not on the list of your allowed IPs.")
            if data['request'] == "MAX_USER_TURN":
                raise MaxUserTurn(
                    "You made more than 60 requests to in.php within 3 seconds. "
                    "Your account is banned for 10 seconds. Ban will be lifted automatically.")

            if data['request'] == "ERROR: NNNN":
                raise NNNNError(
                    'Where NNNN is numeric error code.'
                    'You exceeded request limit and your account is temporary suspended.')
            if data['request'] == "ERROR_BAD_PROXY":
                raise BadProxy(
                    'You can get this error code when sending a captcha via proxy server which is marked '
                    'as BAD by our API')

            task_id = data['request']

            while True:
                await asyncio.sleep(5)
                async with f.post(f"https://2captcha.com/res.php?key={self.api_key}&id={task_id}&json=1&action=get") as lm:
                    data_json = await lm.json()
                if data_json['request'] == "ERROR_CAPTCHA_UNSOLVABLE":
                    raise UnsolvableCaptcha(
                        "We are unable to solve your captcha - three of our workers were unable "
                        "solve it or we didn't get an answer within 90 seconds (300 seconds for "
                        "reCAPTCHA V2). We will not charge you for that request.")
                if data_json['request'] == "REPORT_NOT_RECORDED":
                    raise ReportNotRecorded(
                        "Error is returned to your report request if you already complained lots "
                        "of correctly solved captchas (more than 40%). Or if more than 15 minutes "
                        "passed after you submitted the captcha.")
                if data_json['request'] == "ERROR_IP_ADDRES":
                    raise IpAddressError(
                        "You can receive this error code when registering a pingback (callback) IP "
                        "or domain. This happens if your request is coming from an IP address that "
                        "doesn't match the IP address of your pingback IP or domain.")
                if data_json['request'] == "ERROR_PROXY_CONNECTION_FAILED":
                    raise ProxyConnectionFailed(
                        "You can get this error code if we were unable to load a captcha "
                        "through your proxy server. The proxy will bemarked as BAD by our API "
                        "and we will not accept requests with the proxy during 10 minutes. "
                        "You will receive ERROR_BAD_PROXY code from in.php API endpoint in "
                        "such case.")

                if data_json['request'] != "CAPCHA_NOT_READY":
                    solution = data_json['request']
                    break
            return solution

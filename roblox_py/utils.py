from .exceptions import *
import warnings
import json
from .http_session import Http


class Requests:
    """

    Class Used for Requesting from the Web for roblox_py

    """

    def __init__(self, cookies: str = None):
        self.cookies = cookies
        cookies_list = {'.ROBLOSECURITY': self.cookies}

        self.xcrsftoken = ""
        self.headers = {
            'X-CSRF-TOKEN': self.xcrsftoken,
            'DNT': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'referer': 'www.roblox.com',
            'Origin': 'www.roblox.com',
        }
        self.session = Http(cookies=cookies_list)

    @staticmethod
    def check_status_400(status: int, text):
        if status == 400:
            try:
                if text['errors'][0]['message'] == 'The target user is invalid or does not exist.' or \
                        text['errors'][0]['message'] == 'The user id is invalid.':
                    raise PlayerNotFound(
                        text['errors'][0]['message'])
                if text['errors'][0]['message'] == 'Group is invalid or does not exist.':
                    raise GroupNotFound(
                        text['errors'][0]['message'])
                if text['errors'][0]['message'] == 'Invalid bundle':
                    raise BundleNotFound(
                        text['errors'][0]['message'])
                if text['errors'][0]['message'] == 'Invalid assetId':
                    raise AssetNotFound(
                        text['errors'][0]['message'])
                if text['errors'][0]['message'] == "BadgeInfo is invalid or does not exist.":
                    raise BadgeNotFound(
                        text['errors'][0]['message'])
                else:
                    warnings.warn(
                        text['errors'][0]['message'])
            except KeyError:
                warnings.warn(text)

    @staticmethod
    def request_status(status):
        var = {
            401: Unauthorized,
            429: RateLimited,
            503: ServiceUnavailable,
            500: InternalServiceError,
        }
        return var.get(status)

    async def check_xcrsftoken(self, error_code: int, text, headers):
        if error_code == 403:
            if text['errors'][0]['message'] == 'Token Validation Failed':
                try:
                    self.xcrsftoken = headers['x-csrf-token']
                except KeyError:
                    pass
                return True
            else:
                try:
                    raise Forbidden(
                        text['errors'][0]['message'])
                except KeyError:
                    raise Forbidden(text)

    async def get_xcrsftoken(self):
        """

        Updates the xcrsf-token

        """
        async with self.session as ses:
            async with ses.fetch.post(url="https://auth.roblox.com/") as smth:
                header = smth.headers
                try:
                    xcrsftoken = header["x-csrf-token"]
                    self.xcrsftoken = xcrsftoken
                except KeyError:
                    pass

    async def request(self, url, method=None, data=None, parms: dict = None):
        if method is None:
            method = 'get'
        if self.xcrsftoken == "":
            await self.get_xcrsftoken()
        if data is not None:
            data = json.dumps(data)
        header = {
            'X-CSRF-TOKEN': self.xcrsftoken,
            'DNT': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'referer': 'www.roblox.com',
            'Origin': 'www.roblox.com',
        }
        if method == 'post':
            async with self.session as ses:
                async with ses.fetch.post(url=url, data=data, params=parms, headers=header) as rep:
                    json_text = await rep.json()
                    check = await self.check_xcrsftoken(headers=rep.headers, error_code=rep.status, text=json_text)
                    if check is True:
                        await ses.close_session()
                        await self.request(method=method, data=data, parms=parms, url=url)
                    self.check_status_400(status=rep.status, text=json_text)
                    error = self.request_status(rep.status)
                    if error is not None:
                        try:
                            raise error(json_text['errors'][0]["message"])
                        except KeyError:
                            raise error(json_text)

                return json_text

        if method == 'delete':
            async with self.session as ses:
                async with ses.fetch.delete(url=url, params=parms, headers=header) as rep:
                    json_text = await rep.json()
                    check = await self.check_xcrsftoken(headers=rep.headers, error_code=rep.status, text=json_text)

                    if check is True:
                        await ses.close_session()
                        await self.request(method=method, data=data, parms=parms, url=url)
                    self.check_status_400(status=rep.status, text=json_text)
                    error = self.request_status(rep.status)
                    if error is not None:
                        try:
                            raise error(json_text['errors'][0]["message"])
                        except KeyError:
                            raise error(json_text)
                return json_text
        if method == 'patch':
            async with self.session as ses:
                async with ses.fetch.patch(url=url, data=data, params=parms, headers=header) as rep:
                    json_text = await rep.json()
                    check = await self.check_xcrsftoken(headers=rep.headers, error_code=rep.status, text=json_text)
                    if check is True:
                        await ses.close_session()
                        await self.request(method=method, data=data, parms=parms, url=url)
                    self.check_status_400(status=rep.status, text=json_text)
                    error = self.request_status(rep.status)
                    if error is not None:
                        try:
                            raise error(json_text['errors'][0]["message"])
                        except KeyError:
                            raise error(json_text)
                return json_text
        if method == 'get':
            async with self.session as ses:
                async with ses.fetch.get(url=url, params=parms, headers=header) as rep:
                    json_text = await rep.json()

                    check = await self.check_xcrsftoken(headers=rep.headers, error_code=rep.status, text=json_text)
                    if check is True:
                        await ses.close_session()
                        await self.request(method=method, data=data, parms=parms, url=url)
                    self.check_status_400(status=rep.status, text=json_text)
                    error = self.request_status(rep.status)
                    if error is not None:
                        try:
                            raise error(json_text['errors'][0]["message"])
                        except KeyError:
                            raise error(json_text)
                return json_text

    async def return_headers(self, url, method, data=None, parms=None):
        if self.xcrsftoken == "":
            await self.get_xcrsftoken()
        if data is not None:
            data = json.dumps(data)
        header = {
            'X-CSRF-TOKEN': self.xcrsftoken,
            'DNT': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'referer': 'www.roblox.com',
            'Origin': 'www.roblox.com',
            'RBXAuthenticationNegotiation': 'https://www.roblox.com'}
        if method == 'post':
            async with self.session as ses:
                async with ses.fetch.post(url=url, data=data, params=parms, headers=header) as rep:
                    if rep.status == 400:
                        raise BadRequest()
                    error = self.request_status(rep.status)
                    if error is not None:
                        raise error()
                return rep.headers
        if method == 'patch':
            async with self.session as ses:
                async with ses.fetch.patch(url=url, data=data, params=parms, headers=header) as rep:
                    if rep.status == 400:
                        raise BadRequest()
                    error = self.request_status(rep.status)
                    if error is not None:
                        raise error()
                return rep.headers
        if method == 'get':
            async with self.session as ses:
                async with ses.fetch.get(url=url, data=data, params=parms, headers=header) as rep:
                    if rep.status == 400:
                        raise BadRequest()
                    error = self.request_status(rep.status)
                    if error is not None:
                        raise error()
                return rep.headers
        if method == 'delete':
            async with self.session as ses:
                async with ses.fetch.delete(url=url, data=data, params=parms, headers=header) as rep:
                    if rep.status == 400:
                        raise BadRequest()
                    error = self.request_status(rep.status)
                    if error is not None:
                        raise error()
                return rep.headers

    async def just_request(self, url, method=None, data=None, parms: dict = None):

        if method is None:
            method = 'get'
        if self.xcrsftoken == "":
            await self.get_xcrsftoken()
        if data is not None:
            data = json.dumps(data)
        header = {
            'X-CSRF-TOKEN': self.xcrsftoken,
            'DNT': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'referer': 'www.roblox.com',
            'Origin': 'www.roblox.com',
        }
        if method == 'post':
            async with self.session as ses:
                async with ses.fetch.post(url=url, data=data, params=parms, headers=header) as rep:
                    ok = rep
                    return ok

        if method == 'patch':
            async with self.session as ses:
                async with ses.fetch.patch(url=url, data=data, params=parms, headers=header) as rep:
                    ok = rep
                    return ok
        if method == 'get':
            async with self.session as ses:
                async with ses.fetch.post(url=url, data=data, params=parms, headers=header) as rep:
                    ok = rep
                    return ok

        if method == 'delete':
            async with self.session as ses:
                async with ses.fetch.delete(url=url, data=data, params=parms, headers=header) as rep:
                    ok = rep
                    return ok

    async def html_request(self, url, method, data, parms=None):
        if self.xcrsftoken == "":
            await self.get_xcrsftoken()
        if data is not None:
            data = json.dumps(data)
        header = {
            'X-CSRF-TOKEN': self.xcrsftoken,
            'DNT': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            'Content-type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'referer': 'www.roblox.com',
            'Origin': 'www.roblox.com',
        }
        if method == 'post':
            async with self.session as ses:
                async with ses.fetch.post(url=url, data=data, params=parms, headers=header) as rep:
                    r = await rep.read()
                    if rep.status == 400:
                        raise BadRequest()
                    error = self.request_status(rep.status)
                    if error is not None:
                        raise error()
                return r.decode()
        if method == 'patch':
            async with self.session as ses:
                async with ses.fetch.patch(url=url, data=data, params=parms, headers=header) as rep:
                    r = await rep.read()
                    if rep.status == 400:
                        raise BadRequest()
                    error = self.request_status(rep.status)
                    if error is not None:
                        raise error()
                return r.decode()
        if method == 'get':
            async with self.session as ses:
                async with ses.fetch.get(url=url, data=data, params=parms, headers=header) as rep:
                    r = await rep.read()
                    if rep.status == 400:
                        raise BadRequest()
                    error = self.request_status(rep.status)
                    if error is not None:
                        raise error()
                return r.decode()

        if method == 'delete':
            async with self.session as ses:
                async with ses.fetch.delete(url=url, data=data, params=parms, headers=header) as rep:
                    r = await rep.read()
                    if rep.status == 400:
                        raise BadRequest()
                    error = self.request_status(rep.status)
                    if error is not None:
                        raise error()
                return r.decode()

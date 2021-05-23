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

        self.xcrsftoken = None
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

    async def get_xcrsftoken(self):
        """

        Updates the xcrsftoken

        """
        async with self.session as ses:
            async with ses.fetch.post(url="https://auth.roblox.com/") as smth:
                try:
                    xcrsftoken = smth.headers["X-CSRF-TOKEN"]
                    self.xcrsftoken = xcrsftoken
                except KeyError:
                    self.xcrsftoken = ""

    async def request(self, url, method=None, data=None, parms=None):
        if method is None:
            method = 'get'
        if self.xcrsftoken is None:
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
                    if rep.status == 403:
                        if json_text['errors'][0]['message'] == 'Token Validation Failed':
                            self.xcrsftoken = None
                            await self.get_xcrsftoken()
                            await self.request(url=url, data=data, method=method, parms=parms)
                        else:
                            try:
                                raise Forbidden(
                                    json_text['errors'][0]['message'])
                            except KeyError:
                                raise Forbidden(json_text)

                    if rep.status == 401:
                        try:

                            raise Unauthorized(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise Unauthorized(json_text)
                    if rep.status == 429:
                        try:
                            raise RateLimited(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise RateLimited(json_text)
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable(
                                json_text["errors"][0]['message'])
                        except KeyError:
                            raise ServiceUnavailable(json_text)
                    if rep.status == 500:
                        try:
                            raise InternalServiceError(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise InternalServiceError(json_text)
                    if rep.status == 400:
                        try:
                            if json_text['errors'][0]['message'] == 'The target user is invalid or does not exist.' or \
                                    json_text['errors'][0]['message'] == 'The user id is invalid.':
                                raise PlayerNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Group is invalid or does not exist.':
                                raise GroupNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Invalid bundle':
                                raise BundleNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Invalid assetId':
                                raise AssetNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == "BadgeInfo is invalid or does not exist.":
                                raise BadgeNotFound(
                                    json_text['errors'][0]['message'])
                            else:
                                warnings.warn(
                                    json_text['errors'][0]['message'])
                        except KeyError:
                            warnings.warn(json_text)
                return json_text

        if method == 'delete':
            async with self.session as ses:
                async with ses.fetch.delete(url=url, params=parms, headers=header) as rep:
                    json_text = await rep.json()
                    if rep.status == 403:
                        if json_text['errors'][0]['message'] == 'Token Validation Failed':
                            self.xcrsftoken = None
                            await self.get_xcrsftoken()
                            await self.request(url=url, data=data, method=method, parms=parms)
                        else:
                            try:
                                raise Forbidden(
                                    json_text['errors'][0]['message'])
                            except KeyError:
                                raise Forbidden(json_text)

                    if rep.status == 401:
                        try:
                            raise Unauthorized(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise Unauthorized(json_text)
                    if rep.status == 429:
                        try:
                            raise RateLimited(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise RateLimited(json_text)
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable(
                                json_text["errors"][0]['message'])
                        except KeyError:
                            raise ServiceUnavailable(json_text)
                    if rep.status == 500:
                        try:
                            raise InternalServiceError(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise InternalServiceError(json_text)
                    if rep.status == 400:
                        try:
                            if json_text['errors'][0]['message'] == 'The target user is invalid or does not exist.' or \
                                    json_text['errors'][0]['message'] == 'The user id is invalid.':
                                raise PlayerNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Group is invalid or does not exist.':
                                raise GroupNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Invalid bundle':
                                raise BundleNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Invalid assetId':
                                raise AssetNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == "BadgeInfo is invalid or does not exist.":
                                raise BadgeNotFound(
                                    json_text['errors'][0]['message'])
                            else:
                                warnings.warn(
                                    json_text['errors'][0]['message'])
                        except KeyError:
                            warnings.warn(json_text)
                return json_text
        if method == 'patch':
            async with self.session as ses:
                async with ses.fetch.patch(url=url, data=data, params=parms, headers=header) as rep:
                    json_text = await rep.json()

                    if rep.status == 403:
                        if json_text['errors'][0]['message'] == 'Token Validation Failed':
                            self.xcrsftoken = None
                            await self.get_xcrsftoken()
                            await self.request(url=url, data=data, method=method, parms=parms)
                        else:
                            try:
                                raise Forbidden(
                                    json_text['errors'][0]['message'])
                            except KeyError:
                                raise Forbidden(json_text)

                    if rep.status == 401:
                        try:
                            raise Unauthorized(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise Unauthorized(json_text)
                    if rep.status == 429:
                        try:
                            raise RateLimited(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise RateLimited(json_text)
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable(
                                json_text["errors"][0]['message'])
                        except KeyError:
                            raise ServiceUnavailable(json_text)
                    if rep.status == 500:
                        try:
                            raise InternalServiceError(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise InternalServiceError(json_text)
                    if rep.status == 400:
                        try:
                            if json_text['errors'][0]['message'] == 'The target user is invalid or does not exist.' or \
                                    json_text['errors'][0]['message'] == 'The user id is invalid.':
                                raise PlayerNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Group is invalid or does not exist.':
                                raise GroupNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Invalid bundle':
                                raise BundleNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Invalid assetId':
                                raise AssetNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == "BadgeInfo is invalid or does not exist.":
                                raise BadgeNotFound(
                                    json_text['errors'][0]['message'])
                            else:
                                warnings.warn(
                                    json_text['errors'][0]['message'])
                        except KeyError:
                            warnings.warn(json_text)
                return json_text
        if method == 'get':
            async with self.session as ses:
                async with ses.fetch.get(url=url, params=parms, headers=header) as rep:
                    json_text = await rep.json()

                    if rep.status == 403:
                        if json_text['errors'][0]['message'] == 'Token Validation Failed':
                            self.xcrsftoken = None
                            await self.get_xcrsftoken()
                            await self.request(url=url, data=data, method=method, parms=parms)
                        else:
                            try:
                                raise Forbidden(
                                    json_text['errors'][0]['message'])
                            except KeyError:
                                raise Forbidden(json_text)

                    if rep.status == 401:
                        try:
                            raise Unauthorized(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise Unauthorized(json_text)
                    if rep.status == 429:
                        try:
                            raise RateLimited(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise RateLimited(json_text)
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable(
                                json_text["errors"][0]['message'])
                        except KeyError:
                            raise ServiceUnavailable(json_text)
                    if rep.status == 500:
                        try:
                            raise InternalServiceError(
                                json_text['errors'][0]['message'])
                        except KeyError:
                            raise InternalServiceError(json_text)
                    if rep.status == 400:
                        try:
                            if json_text['errors'][0]['message'] == 'The target user is invalid or does not exist.' or \
                                    json_text['errors'][0]['message'] == 'The user id is invalid.':
                                raise PlayerNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Group is invalid or does not exist.':
                                raise GroupNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Invalid bundle':
                                raise BundleNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == 'Invalid assetId':
                                raise AssetNotFound(
                                    json_text['errors'][0]['message'])
                            if json_text['errors'][0]['message'] == "BadgeInfo is invalid or does not exist.":
                                raise BadgeNotFound(
                                    json_text['errors'][0]['message'])
                            else:
                                warnings.warn(
                                    json_text['errors'][0]['message'])
                        except KeyError:
                            warnings.warn(json_text)
                return json_text

    async def return_headers(self, url, method, data=None, parms=None):
        if self.xcrsftoken is None:
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

                    if rep.status == 401:
                        try:
                            raise Unauthorized()
                        except KeyError:
                            raise Unauthorized()
                    if rep.status == 429:
                        try:
                            raise RateLimited()
                        except KeyError:
                            raise RateLimited()
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable()
                        except KeyError:
                            raise ServiceUnavailable()
                    if rep.status == 500:
                        try:
                            raise InternalServiceError()
                        except KeyError:
                            raise InternalServiceError()
                    if rep.status == 400:
                        raise BadRequest()
                return rep.headers
        if method == 'patch':
            async with self.session as ses:
                async with ses.fetch.patch(url=url, data=data, params=parms, headers=header) as rep:
                    if rep.status == 401:
                        try:
                            raise Unauthorized()
                        except KeyError:
                            raise Unauthorized()
                    if rep.status == 429:
                        try:
                            raise RateLimited()
                        except KeyError:
                            raise RateLimited()
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable()
                        except KeyError:
                            raise ServiceUnavailable()
                    if rep.status == 500:
                        try:
                            raise InternalServiceError()
                        except KeyError:
                            raise InternalServiceError()
                    if rep.status == 400:
                        raise BadRequest()
                return rep.headers
        if method == 'get':
            async with self.session as ses:
                async with ses.fetch.get(url=url, data=data, params=parms, headers=header) as rep:
                    if rep.status == 401:
                        try:
                            raise Unauthorized()
                        except KeyError:
                            raise Unauthorized()
                    if rep.status == 429:
                        try:
                            raise RateLimited()
                        except KeyError:
                            raise RateLimited()
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable()
                        except KeyError:
                            raise ServiceUnavailable()
                    if rep.status == 500:
                        try:
                            raise InternalServiceError()
                        except KeyError:
                            raise InternalServiceError()
                    if rep.status == 400:
                        raise BadRequest()
                return rep.headers
        if method == 'delete':
            async with self.session as ses:
                async with ses.fetch.delete(url=url, data=data, params=parms, headers=header) as rep:
                    if rep.status == 401:
                        try:
                            raise Unauthorized()
                        except KeyError:
                            raise Unauthorized()
                    if rep.status == 429:
                        try:
                            raise RateLimited()
                        except KeyError:
                            raise RateLimited()
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable()
                        except KeyError:
                            raise ServiceUnavailable()
                    if rep.status == 500:
                        try:
                            raise InternalServiceError()
                        except KeyError:
                            raise InternalServiceError()
                    if rep.status == 400:
                        raise BadRequest()
                return rep.headers

    async def just_request(self, url, method=None, data=None, parms: dict = None):

        if method is None:
            method = 'get'
        if self.xcrsftoken is None:
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
        if self.xcrsftoken is None:
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
                    if rep.status == 401:
                        try:
                            raise Unauthorized()
                        except KeyError:
                            raise Unauthorized()
                    if rep.status == 429:
                        try:
                            raise RateLimited()
                        except KeyError:
                            raise RateLimited()
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable()
                        except KeyError:
                            raise ServiceUnavailable()
                    if rep.status == 500:
                        try:
                            raise InternalServiceError()
                        except KeyError:
                            raise InternalServiceError()
                    if rep.status == 400:
                        raise BadRequest()
                return r.decode()
        if method == 'patch':
            async with self.session as ses:
                async with ses.fetch.patch(url=url, data=data, params=parms, headers=header) as rep:
                    r = await rep.read()
                    if rep.status == 401:
                        try:
                            raise Unauthorized()
                        except KeyError:
                            raise Unauthorized()
                    if rep.status == 429:
                        try:
                            raise RateLimited()
                        except KeyError:
                            raise RateLimited()
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable()
                        except KeyError:
                            raise ServiceUnavailable()
                    if rep.status == 500:
                        try:
                            raise InternalServiceError()
                        except KeyError:
                            raise InternalServiceError()
                    if rep.status == 400:
                        raise BadRequest()
                return r.decode()
        if method == 'get':
            async with self.session as ses:
                async with ses.fetch.get(url=url, data=data, params=parms, headers=header) as rep:
                    r = await rep.read()
                    if rep.status == 401:
                        try:
                            raise Unauthorized()
                        except KeyError:
                            raise Unauthorized()
                    if rep.status == 429:
                        try:
                            raise RateLimited()
                        except KeyError:
                            raise RateLimited()
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable()
                        except KeyError:
                            raise ServiceUnavailable()
                    if rep.status == 500:
                        try:
                            raise InternalServiceError()
                        except KeyError:
                            raise InternalServiceError()
                    if rep.status == 400:
                        raise BadRequest()
                return r.decode()

        if method == 'delete':
            async with self.session as ses:
                async with ses.fetch.delete(url=url, data=data, params=parms, headers=header) as rep:
                    r = await rep.read()
                    if rep.status == 401:
                        try:
                            raise Unauthorized()
                        except KeyError:
                            raise Unauthorized()
                    if rep.status == 429:
                        try:
                            raise RateLimited()
                        except KeyError:
                            raise RateLimited()
                    if rep.status == 503:
                        try:
                            raise ServiceUnavailable()
                        except KeyError:
                            raise ServiceUnavailable()
                    if rep.status == 500:
                        try:
                            raise InternalServiceError()
                        except KeyError:
                            raise InternalServiceError()
                    if rep.status == 400:
                        raise BadRequest()
                return r.decode()

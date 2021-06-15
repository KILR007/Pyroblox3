import aiohttp


class Http:
    def __init__(self, cookies=None, trust_env=False):
        """

        A HTTP Class for internal wrapper working for roblox.py

        """
        self.cookies = cookies
        self.trust_env = trust_env

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            cookies=self.cookies, trust_env=self.trust_env)
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def close_session(self):
        await self._session.close()

    @property
    def fetch(self):
        """

        Returns the Concurrent Session

        """
        return self._session

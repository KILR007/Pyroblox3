from .utils import Requests
from .GroupInfo import GroupInfo
from .Auth_Group import GroupAuth
from .PlayerInfo import PlayerInfo
from .exceptions import GroupNotFound, PlayerNotFound, GameNotFound
from .Auth_Player import PlayerAuth
from .BundleInfo import BundleInfo
from .AssetInfo import AssetInfo
from .Join_Game import JoinGame
from .GamepassInfo import GamepassInfo
from .BadgeInfo import BadgeInfo
from .PlaceInfo import PlaceInfo
import aiohttp
import json


class Client:
    """

    Represents a roblox.py Main Client.

    """

    def __init__(self, cookies: str = None):
        self.cookies = cookies
        self.request = Requests(cookies=cookies)

    @staticmethod
    async def get_cookies_from_credentials(username_or_email, password, login_type, token):

        """
        Returns Cookies using Username/Email and Password

        Parameters
        ----------
        username_or_email : str
            User Email/Password to login in
        password : str
            Password of the account
        login_type : str
            login type to login in, can be "email" or "username"
        token : stc
            roblox_py.TwoCaptcha

        """
        login_type = login_type.lower()
        login_dict = None
        if login_type == "email":
            login_dict = {
                "ctype": "Email",
                "cvalue": f"{username_or_email}",
                "password": f"{password}",
            }
        if login_type == "username":
            login_dict = {
                "ctype": "Username",
                "cvalue": username_or_email,
                "password": password
            }
        xcrsftoken = ""
        async with aiohttp.ClientSession() as ses:
            async def update_xcrsftoken():
                async with ses.post(url="https://auth.roblox.com/") as xcsf_req:
                    try:
                        xcrsftoken = xcsf_req.headers["X-CSRF-TOKEN"]
                        return xcrsftoken
                    except KeyError:
                        xcrsftoken = ""
                        return xcrsftoken

            login_dict = json.dumps(login_dict)
            xcrsftoken = await update_xcrsftoken()

            async with ses.post(url=f'https://auth.roblox.com/v2/login', data=login_dict, headers={
                'X-CSRF-TOKEN': xcrsftoken,
                'DNT': '1',
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                'Content-type': 'application/json',
                'Accept': 'application/json',
                'referer': 'www.roblox.com',
                'Origin': 'www.roblox.com',
            }) as f:
                josn = await f.json()

            if f.status == 403:
                if josn['errors'][0]['message'] == "Token Validation Failed":
                    xcrsftoken = await update_xcrsftoken()
                if josn['errors'][0]['message'] == 'You must pass the robot test before logging in.':
                    et = await token.solve(public_key=f'476068BF-9607-4799-B53D-966BE98E2B81')
                    if login_type == "email":
                        login_dict = {
                            "ctype": "Email",
                            "cvalue": username_or_email,
                            "password": password,
                            'captchaToken': et,
                            "captchaProvider": 'PROVIDER_ARKOSE_LABS'}
                    if login_type == 'username':
                        login_dict = {
                            "ctype": "Username",
                            "cvalue": username_or_email,
                            "password": password,
                            'captchaToken': et,
                            "captchaProvider": 'PROVIDER_ARKOSE_LABS'}
                    login_dict = json.dumps(login_dict)
                    xcrsftoken = await update_xcrsftoken()

                    async with ses.post(url=f'https://auth.roblox.com/v2/login', data=login_dict, headers={
                        'X-CSRF-TOKEN': xcrsftoken,
                        'DNT': '1',
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                        'Content-type': 'application/json',
                        'Accept': 'application/json',
                        'referer': 'www.roblox.com',
                        'Origin': 'www.roblox.com',
                    }) as no:
                        ja = await no.json()
                        if no.status == 403:
                            if ja['errors'][0]['message'] == "Token Validation Failed":
                                xcrsftoken = await update_xcrsftoken()
                        try:
                            cookie_dict = {'.ROBLOSECURITY': f"{no.cookies.get('.ROBLOSECURITY').value}",
                                           ".RBXID": f"{no.cookies.get('.RBXID').value}"}
                            return cookie_dict

                        except Exception:
                            return no.cookies

    async def get_group_info(self, group_id: int) -> GroupInfo:
        """

        Returns Group Info Class - Also Calls the update Function

        Parameters
        ----------
        group_id : int
            Group ID

        Returns
        -------
        roblox_py.GroupInfo

        """

        idkdd = isinstance(group_id, str)
        if idkdd:
            raise TypeError(f"{group_id} must be an integer")
        yes = GroupInfo(group_id=group_id, request=self.request)
        await yes.update()
        return yes

    async def get_group_by_name(self, group_name: str) -> list:
        """

        Returns a dict of group by name

        Parameters
        ----------
        group_name : str
            Group Name

        Returns
        -------
        list

        """

        _eep = await self.request.request(
            url=f"https://groups.roblox.com/v1/groups/search/lookup?groupName={group_name}",
            method='get')
        _lis = []
        if _eep['data'] is []:
            raise GroupNotFound
        for data in _eep["data"]:
            idd = data.get("id")
            name = data.get("name")
            e = dict(name=name, id=idd)
            _lis.append(e)
        return _lis

    async def get_user_by_name(self, username: str) -> PlayerInfo:
        """

        Returns Player Info Class By username - Also Calls the update Function

        Parameters
        ----------
        username : str
            Name of the User

        Returns
        -------
        roblox_py.PlayerInfo

        """
        url = f"https://api.roblox.com/users/get-by-username"
        pars = {'username': username}
        json1 = await self.request.request(url=url, parms=pars, method='get')
        if "Id" not in json1.keys():
            raise PlayerNotFound("Username is Invalid")
        else:
            e = PlayerInfo(player_id=json1['Id'], request=self.request)
            await e.update()
            return e

    async def get_user_info(self, Player_Id: int) -> PlayerInfo:
        """

        Returns Player Info Class - Also Calls the update Function

        Parameters
        ----------
        Player_Id : int
            ID of the User

        Returns
        -------
        roblox_py.PlayerInfo

        """
        idkdd = isinstance(Player_Id, str)
        if idkdd:
            raise TypeError(f"{Player_Id} must be an integer")
        yes = PlayerInfo(player_id=Player_Id, request=self.request)
        await yes.update()
        return yes

    async def get_auth_user(self) -> PlayerAuth:
        """
        Returns Authenticated User class

        Returns
        -------
        roblox_py.PlayerAuth

        """
        return PlayerAuth(request=self.request)

    async def get_auth_group(self, Group_Id: int) -> GroupAuth:
        """
        Returns Authenticated Group class

        Parameters
        ----------
        Group_Id : int
            Group Id

        Returns
        -------
        roblox_py.GroupAuth

        """
        idkdd = isinstance(Group_Id, str)
        if idkdd:
            raise TypeError(f"{Group_Id} must be an integer")
        return GroupAuth(group_id=Group_Id, request=self.request)

    async def get_bundle(self, Bundle_ID: int) -> BundleInfo:
        """
        Returns Bundle Info Class

        Parameters
        ----------
        Bundle_ID : int
            Bundle ID

        Returns
        -------
        roblox_py.BundleInfo

        """
        idkdd = isinstance(Bundle_ID, str)
        if idkdd:
            raise TypeError(f"{Bundle_ID} must be an integer")
        yes = BundleInfo(bundle_id=Bundle_ID, request=self.request)
        await yes.update()
        return yes

    async def get_asset(self, Asset_id: int) -> AssetInfo:
        """

        Returns Asset Info Class - Also Calls the update Function

        Parameters
        ----------
        Asset_id : int
            Asset id

        Returns
        -------
        roblox_py.AssetInfo

        """
        idkdd = isinstance(Asset_id, str)
        if idkdd:
            raise TypeError(f"{Asset_id} must be an integer")
        yes = AssetInfo(asset_id=Asset_id, request=self.request)
        await yes.update()
        return yes

    async def get_gamepass(self, gamepass_id: int) -> GamepassInfo:
        """

        Returns Game-pass Info Class - Also Calls the update Function

        Parameters
        ----------
        gamepass_id : int
            gamepass id

        Returns
        -------
        roblox_py.GamepassInfo

        """
        idkdd = isinstance(gamepass_id, str)
        if idkdd:
            raise TypeError(f"{gamepass_id} must be an integer")
        yes = GamepassInfo(gamepass_id=gamepass_id, request=self.request)
        await yes.update()
        return yes

    async def join_game(self, PlaceID: int, roblox_folder_path=None, roblox_game_path=None) -> JoinGame:
        """

        Returns the Join Game Class

        Parameters
        ----------
        PlaceID : int
            Place Id to join
        roblox_folder_path : str
            Roblox Resource Folder Path
        roblox_game_path : str
            Roblox Game Folder Path


        Returns
        -------
        roblox_py.JoinGame

        """
        idkdd = isinstance(PlaceID, str)
        if idkdd:
            raise TypeError(f"{PlaceID} must be an integer")
        return JoinGame(
            game_id=PlaceID,
            request=self.request,
            roblox_folder_path=roblox_folder_path,
            roblox_game_folder_path=roblox_game_path)

    async def get_badge(self, badge_id: int) -> BadgeInfo:
        """
        Returns Badge Info Class - Also Calls the update Function


        Returns
        -------
        roblox_py.BadgeInfo
        """
        idkdd = isinstance(badge_id, str)
        if idkdd:
            raise TypeError(f"{badge_id} must be an integer")
        e = BadgeInfo(badge_id=badge_id, request=self.request)
        await e.update()
        return e

    async def get_place(self, unverise_id) -> PlaceInfo:
        """
        Returns Place Info Class - Also Calls the update Function

        Returns
        -------
        roblox_py.PlaceInfo
        """
        e = PlaceInfo(universe_id=unverise_id, request=self.request)
        await e.update()
        return e

    async def get_place_by_id(self, place_id: int) -> PlaceInfo:
        """
        Returns Place Info Class - Also Calls the update Function

        Returns
        -------
        roblox_py.PlaceInfo
        """
        idkdd = isinstance(place_id, str)
        if idkdd:
            raise TypeError(f"{place_id} must be an integer")
        r = await self.request.request(
            url=f'https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}', method='get')

        if r is []:
            raise GameNotFound("Invalid Game ID")
        e = PlaceInfo(universe_id=r[0]['universeId'], request=self.request)
        await e.update()
        return e

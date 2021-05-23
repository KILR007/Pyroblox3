from .PlayerInfo import PlayerInfo
from .Classes import Time, AccountInformationMetaData, PromotionChannel
from .utils import Requests
from .Twocaptcha import TwoCaptcha


class PlayerAuth:

    def __init__(self, request: Requests):
        self.request = request
        """

        Represents a authenticated User.

        **Parameters**
        ----------
        request : roblox_py.Requests
            Request class to request from
        """

    async def get_self(self) -> PlayerInfo:
        """ Returns Player Info class

        **Returns**
        -------
        roblox_py.PlayerInfo
        """
        e = await self.request.request(url=f'https://users.roblox.com/v1/users/authenticated', method='get')
        a = PlayerInfo(player_id=e['id'], request=self.request)
        await a.update()
        return a

    async def is_premium(self) -> bool:
        """
        Checks if the user is premium or not

        **Returns**
        -------
        bool
            **Returns** true if premium

        """
        e = await self.request.request(url=f'https://www.roblox.com/mobileapi/userinfo', method='get')
        return e['IsPremium']

    async def follow(self, TargetId: int):
        """

        Follows a specific User

        **Parameters**
        ----------
        TargetId : int
            Target's Id to follow

        """
        data = {
            'targetUserId': TargetId
        }
        e = await self.request.request(url=f'https://friends.roblox.com/v1/users/{TargetId}/follow', method='post',
                                       data=data)
        return e

    async def unfollow(self, TargetId: int):
        """

        Unfollows a specific User

        **Parameters**
        ----------
        TargetId : int
            Target's Id to unfollow

        """
        data = {
            'targetUserId': TargetId
        }
        e = await self.request.request(url=f'https://friends.roblox.com/v1/users/{TargetId}/unfollow', method='post',
                                       data=data)
        return e

    async def block(self, TargetId: int):
        """

        Blocks a specific User

        **Parameters**
        ----------
        TargetId : int
            Target's Id to block

        """
        e = await self.request.request(url=f'https://accountsettings.roblox.com/v1/users/{TargetId}/block',
                                       method='post')
        return e

    async def unblock(self, TargetId: int):
        """

        Unblocks a specific User

        **Parameters**
        ----------
        TargetId : int
            Target's Id to block

        """

        e = await self.request.request(url=f'https://accountsettings.roblox.com/v1/users/{TargetId}/unblock',
                                       method='post',
                                       )
        return e

    async def send_friend_request(self, TargetId: int):
        """

        Sends friend request to a specific User

        **Parameters**
        ----------
        TargetId : int
            Target's Id to send request

        """
        data = {
            'targetUserId': TargetId
        }
        e = await self.request.request(url=f'https://friends.roblox.com/v1/users/{TargetId}/request-friendship',
                                       method='post',
                                       data=data)
        return e

    async def unfriend(self, TargetId: int):
        """

        Unfriends a specific User

        **Parameters**
        ----------
        TargetId : int
            Target's Id to unfriend

        """
        data = {
            'targetUserId': TargetId
        }
        e = await self.request.request(url=f'https://friends.roblox.com/v1/users/{TargetId}/unfriend', method='post',
                                       data=data)
        return e

    async def friend_request_count(self) -> int:
        """

        Returns number of friend request

        **Returns**
        -------
        int
            Friend request number
        """
        e = await self.request.request(url=f'https://friends.roblox.com/v1/user/friend-requests/count', method='get',
                                       )
        return e['count']

    async def decline_request(self, TargetId: int):
        """

        Declines a specific User Friend request

        **Parameters**
        ----------
        TargetId : int
            Target's Id to decline to

        """
        data = {
            'targetUserId': TargetId
        }
        e = await self.request.request(url=f'https://friends.roblox.com/v1/users/{TargetId}/decline-friend-request',
                                       method='post',
                                       data=data)
        return e

    async def accept_request(self, TargetId: int):
        """

        Accepts a specific User Friend request

        **Parameters**
        ----------
        TargetId : int
            Target's Id to accept to

        """
        data = {
            'targetUserId': TargetId
        }
        e = await self.request.request(url=f'https://friends.roblox.com/v1/users/{TargetId}/accept-friend-request',
                                       method='post',
                                       data=data)
        return e

    async def is_following(self, TargetId: int):
        """

        Checks if the user is following another user

        **Parameters**
        ----------
        TargetId : int
            Target's Id to check

        **Returns**
        -------
        bool

        """

        data = {"targetUserIds": [TargetId]}
        e = await self.request.request(url=f'https://friends.roblox.com/v1/user/following-exists',
                                       method='post',
                                       data=data)
        return e['followings'][0]['isFollowing']

    async def get_birth_date(self) -> Time:
        """

        Returns Authenticated User Birth date


        **Returns**
        -------
        roblox_py.Classes.Time

        """
        e = await self.request.request(url=f'https://accountinformation.roblox.com/v1/birthdate', method='get')
        return Time(
            yrs=e['birthYear'],
            month=e['birthMonth'],
            day=e['birthDay'])

    async def change_birth_day(self, day, month, year):
        """

        Changes User birth date

        **Parameters**
        ----------
        day : int
            Birth Day
        month : str
            Birth Month
        year : int
            Birth Year
        """

        data = {
            "birthMonth": month,
            "birthDay": day,
            "birthYear": year}
        e = await self.request.request(url=f'https://accountinformation.roblox.com/v1/birthdate', method='post',
                                       data=data)
        return e

    async def get_gender(self):
        """

        Returns Authenticated User Gender


        **Returns**
        -------
        str
            Male/Female

        """
        e = await self.request.request(url='https://accountinformation.roblox.com/v1/gender', method='get')
        val = e['gender']
        if val == 2:
            gender = "Male"
        else:
            gender = "Female"
        return gender

    async def change_gender(self, gender):
        """

        Changes Authenticated User birth date

        **Parameters**
        ----------
        gender : stc
            Male/Female

        """
        data = dict(gender=gender)
        e = await self.request.request(url='https://accountinformation.roblox.com/v1/gender', method='post', data=data)
        return e

    async def get_phone(self):
        """

        Returns Authenticated User Phone number information

        **Returns**
        ----------
        dict

        """

        e = await self.request.request(url='https://accountinformation.roblox.com/v1/phone', method='get')
        return e

    async def change_phone(self, code: int, prefix: int, phone: int, password: str):
        """

                Changes User birth date

                **Parameters**
                ----------
                code : int
                    Country code
                prefix : str
                    Country Phone Number Prefix
                phone : int
                    Phone Number to change
                password : str
                    Password of the Authenticated Account
        """
        data = {
            "countryCode": code,
            "prefix": prefix,
            "phone": phone,
            "password": password
        }
        e = await self.request.request(url='https://accountinformation.roblox.com/v1/phone', method='post', data=data)
        return e

    async def metadata(self) -> AccountInformationMetaData:
        """
        Returns Meta Data About the Authenticated Account

        **Returns**
        -------
        roblox_py.Classes.AccountInformationMetaData

        """

        e = await self.request.request(url=f'https://accountinformation.roblox.com/v1/metadata', method='get')
        return AccountInformationMetaData(item=e)

    async def delete_phone(self, code: int, prefix: int, phone: int, password: str):
        """
        Delete Phone From the account

        **Parameters**
        ----------
        code : int
            Country code
        prefix : str
            Country Phone Number Prefix
        phone : int
            Phone Number to change
        password : str
            Password of the Authenticated Account

        """
        data = {
            "countryCode": code,
            "prefix": prefix,
            "phone": phone,
            "password": password
        }
        e = await self.request.request(url='https://accountinformation.roblox.com/v1/phone/delete', method='post',
                                       data=data)
        return e

    async def verify_phone(self, code):
        """
        Verifies Phone

        **Parameters**
        ----------
        code : int
            Country code

        """
        data = dict(code=code)
        e = await self.request.request(url='https://accountinformation.roblox.com/v1/phone/verify', method='post',
                                       data=data)
        return e

    async def get_promotion_channel(self) -> PromotionChannel:
        """
        Returns Promotion Channel of the User

        **Returns**
        -------
        roblox_py.Classes.PromotionChannel

        """
        e = await self.request.request(url='https://accountinformation.roblox.com/v1/promotion-channels', method='get')
        return PromotionChannel(iteam=e)

    async def change_promotion_channel(self, **kwargs):

        """
        Changes User's Promotion Channel

        """

        facebook = kwargs.get('facebook', None)
        twitter = kwargs.get('twitter', None)
        youtube = kwargs.get('youtube', None)
        twitch = kwargs.get('twitch', None)
        privacy = kwargs.get('privacy', None)
        data = {
            "facebook": facebook,
            "twitter": twitter,
            "youtube": youtube,
            "twitch": twitch,
            "promotionChannelsVisibilityPrivacy": privacy
        }

        e = await self.request.request(url='https://accountinformation.roblox.com/v1/phone/promotion-channels',
                                       method='post',
                                       data=data,
                                       )
        return e

    async def get_star_code(self):
        """
        Returns which current star code a user uses

        """
        e = await self.request.request(url=f'https://accountinformation.roblox.com/v1/star-code-affiliates',
                                       method='get')
        return e

    async def change_star_code(self, code):
        """
        Changes User's Star Code

        Parameter
        ---------
        code : str
            Star Code


        """
        data = {"code": code}
        e = await self.request.request(url=f'https://accountinformation.roblox.com/v1/star-code-affiliates',
                                       method='post', data=data)
        return e

    async def delete_star_code(self):
        """
        Deletes User Current Star Code
        """

        e = await self.request.request(url=f'https://accountinformation.roblox.com/v1/star-code-affiliates',
                                       method='delete',
                                       )
        return e

    async def get_chat_app_privacy(self):

        """

        Returns  User Chat App Privacy Level

        """

        e = await self.request.request(url=f'https://accountsettings.roblox.com/v1/app-chat-privacy', method='get')
        return e['appChatPrivacy']

    async def change_chat_app_privacy(self, privacy: str):
        """
        Changes User's Chat App Privacy Level

        Parameter
        ---------
        privacy : str
            Privacy Level

        """
        data = {
            "appChatPrivacy": privacy
        }
        e = await self.request.request(url=f'https://accountsettings.roblox.com/v1/app-chat-privacy', method='post',
                                       data=data)
        return e

    async def get_game_app_privacy(self):

        """

        Returns  User Game App Privacy Level

        """

        e = await self.request.request(url=f'https://accountsettings.roblox.com/v1/game-chat-privacy', method='get')
        return e['gameChatPrivacy']

    async def change_game_app_privacy(self, privacy: str):
        """
        Changes User's Game App Privacy Level

        Parameter
        ---------
        privacy : str
            Privacy Level

        """
        data = {
            "gameChatPrivacy": privacy
        }
        e = await self.request.request(url=f'https://accountsettings.roblox.com/v1/game-chat-privacy', method='post',
                                       data=data)
        return e

    async def get_inventory_privacy(self):
        """

        Returns  User Inventory  Privacy Level

        """
        e = await self.request.request(url=f'https://accountsettings.roblox.com/v1/inventory-privacy', method='get',
                                       )
        return e['inventoryPrivacy']

    async def change_inventory_privacy(self, privacy: str):
        """
        Changes User's Inventory Privacy Level

        Parameter
        ---------
        privacy : str
            Privacy Level

        """
        data = {
            "inventoryPrivacy": privacy
        }
        e = await self.request.request(url=f'https://accountsettings.roblox.com/v1/inventory-privacy', method='post',
                                       data=data)
        return e

    async def get_private_message_privacy(self):
        """

        Returns  User Message Privacy Level

        """
        e = await self.request.request(url=f"https://accountsettings.roblox.com/v1/private-message-privacy",
                                       method='get')
        return e['privateMessagePrivacy']

    async def change_private_message_privacy(self, privacy: str):
        """
        Changes User's Message Privacy Level

        Parameter
        ---------
        privacy : str
            Privacy Level

        """
        data = {"privateMessagePrivacy": privacy}
        e = await self.request.request(url=f"https://accountsettings.roblox.com/v1/private-message-privacy",
                                       method='post', data=data)
        return e

    async def get_email(self) -> dict:
        """

        Returns  User's Email

        """
        e = await self.request.request(url='https://accountsettings.roblox.com/v1/email', method='get')
        return e

    async def change_email(self, new_email, password):
        """
        Changes User's Email
        Parameter
        ---------
        new_email : str
            New User Email

        password : stc
            User Password
        """
        data = {"password": password, "emailAddress": new_email}
        e = await self.request.request(url='https://accountsettings.roblox.com/v1/email', method='post', data=data)
        return e

    async def get_trade_privacy(self) -> str:
        """

        Returns  User Trade  Privacy Level

        """
        e = await self.request.request(url=f"https://accountsettings.roblox.com/v1/private-message-privacy",
                                       method='get',
                                       )
        return e['tradePrivacy']

    async def change_trade_privacy(self, privacy: str):
        """
        Changes User's Trade Privacy Level

        Parameter
        ---------
        privacy : str
            Privacy Level

        """
        data = {'tradePrivacy': privacy}
        e = await self.request.request(url=f"https://accountsettings.roblox.com/v1/private-message-privacy",
                                       method='post',
                                       data=data)
        return e

    async def claim_group_owner(self, group_id: int):
        """

        Claims a joined group

        Parameter
        ---------
        group_id : int
            Group ID


        """
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/claim-ownership',
                                       method='post')
        return r

    async def set_primary_group(self, group_id: int):
        """

        Sets  a group primary Group

        Parameter
        ---------
        group_id : int
            Group ID


        """
        data = {
            "groupId": group_id}
        r = await self.request.request(url='https://groups.roblox.com/v1/user/groups/primary', data=data, method='post')
        return r

    async def delete_primary_group(self):
        """

        Deletes Primary Group

        """
        r = await self.request.request(url='https://groups.roblox.com/v1/user/groups/primary', method='delete')
        return r

    async def get_robux(self) -> int:
        """

        Returns Amount of Robux in an account

        """
        e = await self.request.request(url=f'https://users.roblox.com/v1/users/authenticated', method='get')
        p = await self.request.request(url=f'https://economy.roblox.com/v1/users/{e["id"]}/currency', method='get')
        return p['robux']

    async def buy(self, product_id: int):
        """

        Buys a product using product id

        Parameter
        ---------
        product_id : int
            Product ID

        """
        ee = self.request.request(
            url=f'https://economy.roblox.com/v2/user-products/{product_id}/purchase',
            method='post')
        return ee

    async def change_username(self, new_username: str, password: str):

        """
        Changes Account Username

        Parameter
        ---------
        new_username : str
            New Username for the account
        password : str
            Password of the account
        """

        data = {"username": f"{new_username}", "password": f"{password}"}
        ee = await self.request.request(url=f'https://auth.roblox.com/v2/username', method='post', data=data)
        return ee

    async def post_message_in_wall(self, group_id, message: str, captcha_token: TwoCaptcha = None):
        """

        Posts a message in the wall of the group

        Parameter
        ---------
        group_id : int
            Group Id
        message : str
            Wall Message to post
        captcha_token : str
            roblox_py.TwoCaptcha
        """
        data = {"body": f"{message}"}

        a = await self.request.just_request(url=f'https://groups.roblox.com/v2/groups/{group_id}/wall/posts', data=data,
                                            method='post')
        json_text = await a.json()
        if a.status == 403:
            if json_text['errors'][0]['message'] == "Captcha must be solved.":
                et = await captcha_token.solve(public_key=f'63E4117F-E727-42B4-6DAA-C8448E9B137F')
                data = {
                    "body": "string",
                    "captchaToken": f"{et}",
                    "captchaProvider": "PROVIDER_ARKOSE_LABS"}
                b = await self.request.just_request(url=f'https://groups.roblox.com/v2/groups/{group_id}/wall/posts',
                                                    data=data, method='post')
                jj = await b.json()
                return jj
        else:
            return json_text

    async def join_group(self, group_id, captcha_token: TwoCaptcha = None):
        """

        Joins A User Group

        Parameter
        ---------
        group_id : int
            Group Id
        captcha_token : str
            roblox_py.TwoCaptcha

        """

        data = {}

        a = await self.request.just_request(url=f'https://groups.roblox.com/v1/groups/{group_id}/users', data=data,
                                            method='post')
        json_text = await a.json()
        if a.status == 403:
            if json_text['errors'][0]['message'] == "You must pass the captcha test before joining this group.":
                et = await captcha_token.solve(public_key=f'63E4117F-E727-42B4-6DAA-C8448E9B137F')
                data = {
                    "captchaToken": f"{et}",
                    "captchaProvider": "PROVIDER_ARKOSE_LABS"}
                b = await self.request.just_request(url=f'https://groups.roblox.com/v1/groups/{group_id}/users',
                                                    data=data, method='post')
                jj = await b.json()
                return jj
        else:
            return json_text

    async def redeem_game_card(self, game_code: int, captcha_token: TwoCaptcha):

        """

        Redeems a game-card

        Parameter
        ---------
        game_code : int
            Game code to redeem
        captcha_token : str
            roblox_py.TwoCaptcha
        """
        data = {"pinCode": f"{game_code}"}

        a = await self.request.just_request(url=f'https://billing.roblox.com/v1/gamecard/redeem', data=data,
                                            method='post')
        json_text = await a.json()
        if a.status == 403:
            if json_text['errors'][0]['message'] == "Captcha":
                et = await captcha_token.solve(public_key=f'1B154715-ACB4-2706-19ED-0DC7E3F7D855')
                data = {
                    "pinCode": f"{game_code}",
                    "captchaToken": f"{et}",
                    "captchaProvider": "PROVIDER_ARKOSE_LABS"}
                b = await self.request.just_request(url=f'https://billing.roblox.com/v1/gamecard/redeem',
                                                    data=data, method='post')

                jj = await b.json()
                return jj
        else:
            return json_text

    async def change_display_name(self, display_name: str):
        """
        Changes User's Display Name (Limited to germany only, as of now)
        """
        re = await self.request.request(url=f'https://users.roblox.com/v1/users/authenticated')
        user_id = re['id']
        data = {"newDisplayName": f"{display_name}"}
        _ok = await self.request.request(url=f"https://users.roblox.com/v1/users/{user_id}/display-names", data=data,
                                         method="patch")
        return _ok

    # .. TODO: get friend request

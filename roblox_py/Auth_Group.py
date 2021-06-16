from .GroupInfo import GroupInfo
from .Classes import PartialInfo
from .utils import Requests


class GroupAuth:

    def __init__(self, request: Requests, group_id: int):
        """
        Represents a authenticated Group.

         **Parameters**
        ----------
        request : roblox_py.Requests
            Request class to request from
        group_id : int
            Group Id
        """
        self.request = request
        self.group_id = group_id

    async def group_info(self) -> GroupInfo:
        """ Returns Group Info class which contains more info about the group

            **Returns**
            -------
            roblox.py.GroupInfo
        """
        group_class = GroupInfo(group_id=self.group_id, request=self.request)
        await group_class.update()
        return group_class

    async def pay(self, user_id: int, amount: int):
        """ Pays the user robux from the group

        **Parameters**
        ----------
        user_id : int
            User's id to pay
        amount : int
            Amount to pay

        """
        data = {
            "PayoutType": "FixedAmount",
            "Recipients": [
                {
                    "recipientId": user_id,
                    "recipientType": "User",
                    "amount": amount
                }
            ]
        }
        amount_paid = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/payouts',
                                       data=data, method="post")
        return amount_paid

    async def change_description(self, description: str = None):
        """ Changes group description

        **Parameters**
        ----------
        description : str
            New description

         """
        data = {"description": description}
        description_request = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.group_id}/description",
                                       method='patch', data=data)
        return description_request

    async def change_shout(self, status: str = None):
        """ Posts a new group shout

        **Parameters**
        ----------
        status : str
            New shout

        """
        data = {"message": status}
        changed_shout = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.group_id}/status",
                                       method='patch', data=data)
        return changed_shout

    async def decline_join_request(self, user_id: int):
        """ Declines user join request

        **Parameters**
        ----------
        user_id : int
            User id
        """

        data = {"UserIds": [user_id]}
        join_request_declined = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/join-requests',
                                       method='delete', data=data)
        return join_request_declined

    async def accept_join_request(self, user_id: int):
        """ Accepts user join request

        **Parameters**
        ----------
        user_id : int
            User id
        """

        data = {"UserIds": [user_id]}
        join_request_accepted = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/join-requests',
                                       method='post', data=data)
        return join_request_accepted

    async def pay_percentage(self, user_id: int, percent: int):
        """ Pays the user robux percentage from the group

        **Parameters**
        ----------
        user_id : int
            User's id to pay
        percent : int
            Amount to pay robux percentage

        """
        data = {
            "PayoutType": "FixedAmount",
            "Recipients": [
                {
                    "recipientId": user_id,
                    "recipientType": "User",
                    "amount": percent
                }
            ]
        }
        paid_percentage = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/payouts',
                                       data=data, method="post")
        return paid_percentage

    async def change_rank(self, user_id: int, roleId: int):
        """ Changes a user Role

        **Parameters**
        ----------
        user_id : int
            User's id to pay
        roleId : int
           New role id

        """

        data = {
            'roleId': roleId
        }
        changed_rank = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/users/{user_id}',
                                       method="patch", data=data)
        return changed_rank

    async def get_funds(self) -> int:
        """ Gets Group's funds

        **Returns**
        -------
        int
            Group's Robux

        """
        group_funds = await self.request.request(url=f'https://economy.roblox.com/v1/groups/{self.group_id}/currency',
                                       method='get')
        return group_funds['robux']

    async def change_owner(self, user_id: int):
        """ Changes Group Owner


        **Parameters**
        ----------
        user_id : int
            User id

        """
        data = {"userId": user_id}
        changed_owner = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/change-owner',
                                       method='post',
                                       data=data)
        return changed_owner

    async def exile(self, user_id: int):
        """
        Removes User from a group

        **Parameters**
        ----------
        user_id : int
            User's id to remove
        """
        exiled_user = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/users/{user_id}',
                                       method='delete')
        return exiled_user

    async def get_social_link(self) -> dict:
        """
        Gets social links of the group

        **Returns**
        -------
        dict
            Dict  containing all social links

        """
        social_links = await self.request.request(
            url=f'https://groups.roblox.com/v1/groups/{self.group_id}/social-links',
            method='get')
        return social_links['data'][0]

    async def change_social_link(self, social_type: str, url: str, title: str):
        """
        Posts a Social link

        **Parameters**
        ----------
        social_type : str
            Social link type (i.e facebook,twitter)
        url : str
            Social Media link
        title : str
            Social Media Title
        """
        data = {
            "type": social_type,
            "url": url,
            "title": title
        }
        changed_social_link = self.request.request(
            url=f'https://groups.roblox.com/v1/groups/{self.group_id}/social-links',
             method='post',
            data=data)
        return changed_social_link

    async def delete_all_post(self, user_id: int):
        """
        Removes all post from the user

        **Parameters**
        ----------
        user_id : int
            User's id to remove posts
        """
        deleted_user_post = await self.request.request(
            url=f'https://groups.roblox.com/v1/groups/{self.group_id}/wall/users/{user_id}/posts', method='delete')
        return deleted_user_post

    async def exile_and_remove_posts(self, user_id: int):
        """
        Removes all posts from the user & exiles him

        **Parameters**
        ----------
        user_id : int
            ID of the user
        """
        removed_posts = await self.delete_all_post(user_id=user_id)
        exiled_user = await self.exile(user_id=user_id)
        return exiled_user, removed_posts

    async def get_roles_info(self) -> list:
        """
        Gets group's role info (ID,name)
        """
        link = f"https://groups.roblox.com/v1/groups/{self.group_id}/roles"
        get_roles = await self.request.request(url=link, method='get')
        _list = []
        for info in get_roles['roles']:
            role_name = info.get('name')
            role_id = info.get('id')
            inst = PartialInfo(name=role_name, id=role_id)
            _list.append(inst)
        return _list

    # TODO: get join request

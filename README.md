
# **roblox.py**

[![Support Server](https://img.shields.io/discord/591914197219016707.svg?label=Discord&logo=Discord&colorB=7289da&style=for-the-badge)](https://discord.gg/vpEv3HJ)  [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/KILR007/pyrblx/blob/master/LICENSE.txt)  [![Downloads](https://static.pepy.tech/badge/roblox.py)](https://static.pepy.tech/badge/roblox.py)  
**Modern async API wrapper for Roblox with game client support**

### Key Features
- Easy to Use
- Alot of Features
- Asynchronous
- Game client support
- Few Dependencies

#### Installation
###### [PIP INSTALLATION](https://pypi.org/project/roblox.py/)
````bash
pip install roblox.py
````

###### [Source Installation](https://github.com/KILR007/roblox.py/)
````bash
pip install git+https://github.com/KILR007/roblox.py
````  
*[git](https://git-scm.com/) is required to install from source, please install it [here](https://git-scm.com/downloads)*

### Quick Examples

#### Playerinfo example
````python
import asyncio
from roblox_py import Client
client = Client()
async def main():
    user = await client.get_user_info(925355805) # User Id here
    print(await user.friends())
    print(user.name)
    print(user.created_at)
    print(await user.promotion_channel())
    print(await user.following_count())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
````
#### Groupinfo example

````python
import asyncio
from roblox_py import Client
client = Client()
async def main():
    group = await client.get_group_info(4680721) # Group Id here
    print(await group.allies())
    print(group.name)
    print(group.owner)
    print(await group.enemies())
    print(await group.games())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
````
#### Game Join Example

````python
import asyncio
from roblox_py import Client
client = Client(cookies="Your Cookies here")
async def main():
    auth_game = await client.join_game(6237170604) # takes in server ID
    await auth_game.join_game() #joins an random server
    await asyncio.sleep(30) #wait for the game to load (depends on u)
    await auth_game.kill_game() #closes the roblox
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
````

#### Authenticated User Example

````python
import asyncio
from roblox_py import Client
client = Client(cookies="Your Cookies here")
async def main():
    auth_user = await client.get_auth_user()
    await auth_user.follow(TargetId=1) # input user ID
    await auth_user.send_friend_request(TargetId=2) # input user ID
    await auth_user.claim_group_owner(2323) # clamins group if possible

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
````

#### Authenticated  Group Example

````python
import asyncio
from roblox_py import Client
client = Client(cookies="Your Cookies here")
async def main():
    auth_group = await client.get_auth_group(3232) # group id of which u wanna take actions with
    await auth_group.pay(user_id=1,amount=23) # Pays 23 robux to the user with the spcified user_id
    await auth_group.change_description(description="very cool description")
    print(await auth_group.get_funds())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
````
##### *For more example see Example Folder*

### TODO LIST
- Improve Code Speed
- Write Docs (ofc)
- Improve Code quality
- PEP8 Code
- Context Manager In game client

### Important Links
- [Docs](https://kilr007.github.io/roblox.py)
- [Examples](https://github.com/KILR007/roblox.py/tree/master/Examples)
- [Discord Server](https://discord.gg/vpEv3HJ)
- [GitHub](https://github.com/KILR007/roblox.py)

### Dev Note
- the library is still in beta, bugs may occur

### Credits
- [nsg](https://github.com/nsg-mfd) :: Helped in game client & Endpoints.
- Inspired from [robloxapi](https://github.com/iranathan/robloxapi).
- Took some help from [rockblox](https://pypi.org/project/rockblox/) in game client.

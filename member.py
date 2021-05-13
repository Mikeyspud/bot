import discord
import requests
from constants import Constants

class Member:

    xp_cap = 100
    ps2_api = "http://census.daybreakgames.com/get/ps2:v2/character/"

    def __init__(self, _id: int, **kwargs):

        self._id = _id
        self.level = kwargs.get("level", 1)
        self.expierence = kwargs.get("expierence", 0)
        self.history = kwargs.get("history", list())
        self.ps2_char = kwargs.get("ps2_char")

    def __eq__(self, other):

        return self._id == other

    def __hash__(self):

        return hash(self._id)

    def __str__(self):

        message = f"""
        Member ID: {self._id}
        Claimed: {self.claimed}
        Level: {self.level}
        XP: {self.xp_to_next_level()}
        """

        return message

    def __repr__(self):

        return f"{self.__class__.__name__}(**{vars(self)})"

    def claimed(self):

        return self.ps2_char is not None
    
    def xp_to_next_level(self):

        return self.xp_cap - self.expierence

    def claim(self, name: str):

        params = {"name.first_lower": name.lower(), "c:resolve": "outfit"}
        response = self._api_request(self.ps2_api, params=params).json()["character_list"][0]
        if not self.verify_faction(faction_id=response["faction_id"]):
            raise InvalidFaction
        if not self.verify_outfit(outfit_id=response["outfit"]["outfit_id"]):
            raise InvalidOutfit
        self.ps2_char = name

    def verify_faction(self, faction_id: str) -> bool:

        return faction_id == Constants.faction_identifier()

    def verify_outfit(self, outfit_id: int) -> bool:

        return outfit_id == Constants.outfit_identifier()

    def unclaim(self):

        self.ps2_char = None

    def embed(self):

        embed = discord.Embed(
            title="BJay Signup Bot",
            description="Member Information",
            color=0x2117db
        )
        return embed

    def award(self, xp: int):

        while xp < self.xp_to_next_level():
            self.level += 1
            xp -= self.xp_cap

    def _api_request(self, url: str, **kwargs):

        method = kwargs.get("method", "get")
        request = {"get": requests.get, "post": requests.post}
        response = request[method](url=url, **kwargs)
        if "text/html" in response.headers["Content-Type"]:
            raise requests.ConnectionError
        return response


class InvalidFaction(Exception):

    pass


class InvalidOutfit(Exception):

    pass

if __name__ == "__main__":

    member = Member(_id=1)
    print(member)
    member.award(150)
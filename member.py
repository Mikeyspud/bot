import discord
import requests
from database import Database
from constants import Constants
import pymongo.collection, pymongo.errors

class _Member:

    def __init__(
        self,
        _id: int,
        _discord_name: str,
        participation_points: int = 0,
        history: list = list(),
        ps2_char: str = None
    ):

        self._id = _id
        self._discord_name = _discord_name
        self.participation_points = participation_points
        self.history = history
        self.ps2_char = ps2_char

    def __eq__(self, other):

        return self._id == other._id

    def __hash__(self):

        return hash(self._id)

    def __str__(self):

        message = f"""
        Member ID: {self._id}
        Claimed: {self.claimed}
        Points: {self.participation_points}
        """

        return message

    def __repr__(self):

        return f"{self.__class__.__name__}(**{vars(self)})"

    @property
    def embed_string__(self) -> str:

        if self.claimed:
            return f"**{self.ps2_char}**"
        else:
            return self._discord_name

    def is_loaded(self) -> bool:

        return "_id" in vars(self)

    def claim(self, ps2_name: str):

        if self.is_loaded():
            self.ps2_char = ps2_name
        else:
            raise self.NotLoaded

    def unclaim(self):

        if self.is_loaded():
            self.ps2_char = None
        else:
            raise self.NotLoaded

    def award(self, points: int):

        if self.is_loaded():
            self.participation_points += points
        else:
            raise self.NotLoaded

    def save(self, database):

        document = {
            "_id": self._id,
            "_discord_name": self._discord_name,
            "participation_points": self.participation_points,
            "history": self.history,
            "ps2_char": self.ps2_char
        }

        try:
            database.insert_one(document)
        except pymongo.errors.DuplicateKeyError:
            database.update_one({"_id": self._id}, {"$set": document})

    @property
    def __last_ops(self):

        if len(self.history) == 0:
            return "No Recorded Ops"
        else:
            return self.history[-1]

    @property
    def claimed(self):

        return self.ps2_char != None

    def embed(self):

        embed = discord.Embed(
            title="BJay Signup Bot",
            description="Member Information",
            color=0x2117db
        )
        embed.set_author(
            name="Get Off My Base Peasants",
            url=Constants.outfit_url(),
            icon_url=Constants.outfit_icon()
        )
        if self._discord_name:
            embed.add_field(
                name="Discord Name",
                value=self._discord_name
            )

        if self.ps2_char:
            embed.add_field(
                name="Planetside 2 Character",
                value=self.ps2_char
            )
        else:
            embed.add_field(
                name="Planetside 2 Character",
                value="Unclaimed"
            )
        embed.add_field(
            name="Participation Points",
            value=self.participation_points
        )
        embed.add_field(
            name="Last Recorded Ops",
            value=self.__last_ops
        )
        
        return embed

    class InvalidCharacterName(Exception):

        pass

    class Fuck(Exception):

        pass

    class NotLoaded(Exception):

        pass


class Member:

    PS2_API = "http://census.daybreakgames.com/get/ps2:v2/character/"

    def __init__(self, database: pymongo.collection):

        self.database = database

    def create(self, member: discord.Member) -> _Member:

        _id = member.id
        _discord_name = member.display_name
        participation_points = 0
        history = list()
        ps2_char = None

        member = _Member(
            _id=_id,
            _discord_name=_discord_name,
            participation_points=participation_points,
            history=history,
            ps2_char=ps2_char
        )

        try:
            self.database.insert_one(vars(member))
        except pymongo.errors.DuplicateKeyError:
            pass

        return member

    def load(self, member: discord.Member):

        document = self.database.find_one({"_id": member.id})
        if document:
            return _Member(**document)
        else:
            raise self.DatabaseEntryDoesntExist

    @classmethod
    def _api_request(cls, url: str, **kwargs):

        method = kwargs.get("method", "get")
        request = {"get": requests.get, "post": requests.post}
        response = request[method](url=url, **kwargs)
        if "text/html" in response.headers["Content-Type"]:
            raise requests.ConnectionError
        return response

    @classmethod
    def get_member_id_by_name(cls, name: str) -> str:

        parameters = {"name.first_lower": name.lower()}
        response = cls._api_request(url=cls.PS2_API, params=parameters).json()
        if response["returned"] == 0:
            raise cls.InvalidCharacterName
        return response["character_list"][0]["character_id"]


    class InvalidCharacterName(Exception):

        pass


    class DatabaseEntryDoesntExist(Exception):

        pass
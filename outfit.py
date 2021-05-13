import requests
import pymongo.errors
from database import Database
from event import Event

class Outfit:

    ps2_api = "http://census.daybreakgames.com/get/ps2:v2/outfit/"

    def __init__(self, name: str):

        self.name = name
        for key, value in self._fetch_properties_with_name().items():
            self.__setattr__(key, value)
        self.events = set()
        self.database = Database().bjay

    def add_event(self, event: Event):

        if event in self.events:
            raise EventExists

        self.events.add(event)

    def add_member(self, member):

        db_member = self.database.members.find_one({"_id": member._id})
        if db_member:
            for key, value in db_member.items():
                member.__setattr__(key, value)
        self.members.append(member)

        try:
            self.database.members.insert_one(vars(member))
        except pymongo.errors.DuplicateKeyError:
            self.database.members.update_one({"_id": member._id}, {"$set": vars(member)})

    def event(self, _id: int):

        return [event for event in self.events if _id == event]

    def _fetch_properties_with_name(self) -> dict:

        parameters = {"name": self.name}
        response = self._api_request(url=self.ps2_api, params=parameters)
        if len(response.json()["outfit_list"]) != 1:
            raise OutfitNameException
        return response.json()["outfit_list"][0]

    def _api_request(self, url: str, **kwargs):

        method = kwargs.get("method", "get")
        request = {"get": requests.get, "post": requests.post}
        response = request[method](url=url, **kwargs)
        if "text/html" in response.headers["Content-Type"]:
            raise requests.ConnectionError
        return response


class EventExists(Exception):

    pass


class OutfitNameException(Exception):

    pass

if __name__ == "__main__":

    outfit = Outfit(name="Get Off My Base Peasants")
    print(vars(outfit))
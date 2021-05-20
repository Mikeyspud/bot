import requests
import pymongo.errors
from database import Database
from constants import Constants

class Outfit:

    SERVICE_ID = Constants.api_service_id()
    PS2_API = f"http://census.daybreakgames.com/s:{SERVICE_ID}/get/ps2:v2/outfit/"

    def __init__(self, name: str):

        self.__name = name.lower()
        self.name = None
        self.name_lower = None
        self.alias = None
        self.members = set()
        self.events = set()
        for key, value in self._fetch_properties_with_name().items():
            if isinstance(value, list) and key == "members":
                self.members = self.members.union(set([member["character_id"] for member in value]))
            elif key in vars(self):
                self.__setattr__(key, value)

    def _fetch_properties_with_name(self) -> dict:

        parameters = {
            "name_lower": self.__name, 
            "c:resolve": "member"
        }
        response = self._api_request(url=self.PS2_API, parameters=parameters)
        if len(response.json()["outfit_list"]) != 1:
            raise OutfitNameException
        return response.json()["outfit_list"][0]

    def _api_request(self, url: str, parameters: dict, **kwargs):

        # A dict of all the methods. Lets us call a requests.METHOD function
        # depending on the method supplied through **kwargs["method"].
        # The alternative is a messy if function as more methods are required
        request = {
            "get": requests.get, 
            "post": requests.post
        }
        method = kwargs.get("method", "get")
        response = request[method](url=url, params=parameters)

        if "text/html" in response.headers.get("Content-Type"):
            raise requests.ConnectionError

        return response


class EventExists(Exception):

    pass


class OutfitNameException(Exception):

    pass

if __name__ == "__main__":

    outfit = Outfit(name="Get Off My Base Peasants")
    print(vars(outfit))
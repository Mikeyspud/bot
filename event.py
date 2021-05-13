import discord
import datetime


class Event:

    def __init__(self, _id: int, name: str, start_time: str, duration: int = 2, **kwargs):

        self._id = _id
        self.__name = name
        self.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        self.groups = set()

    def __str__(self):

        message = f"""
            name: {self.name}
            start_time = {self.start_time}
        """
        return message

    def __eq__(self, other):

        return self._id == other._id

    def __hash__(self):

        return hash(self._id)

    @property
    def name(self) -> str:

        return self.__name.title()

    def embed(self) -> discord.Embed:

        embed = discord.Embed(
            title=f"Event {self.name}",
            description="BJay Signup Bot",
            color=0x2117db
        )
        embed.set_author(
            name=f"[{self.client.outfit.alias}] {self.client.outfit.name}", 
            icon_url="https://www.outfit-tracker.com/usercontent/outfits/logo/37573720558810750.png"
        )
        embed.add_field(
            name="Start Time", 
            value=self.start_time
        )
        if self.squad_lead:
            embed.add_field(name="Squad Leader", value=self.squad_lead)
        if self.fireteam_lead:
            embed.add_field(name="Fireteam Lead", value=self.fireteam_lead)

        yield embed

        for group in self.groups:
            yield group.embed

    def add_group(self, name: str, **kwargs):

        self.groups.add(Group(name, **kwargs))

    def group(self, name: str):

        return [group for group in self.groups if name == group][0]


class Group:

    def __init__(self, name: str, **kwargs):

        self.__name = name
        self.participants = set()

    def __eq__(self, other):

        return self.name == other

    def __hash__(self):

        return hash(self.name)

    @property
    def name(self) -> str:

        return self.__name.title()

    def embed(self) -> discord.Embed:

        embed = discord.Embed(
            title=f"Group {self.name}",
            description="BJay Signup Bot",
            color=0xebc20a
        )
        embed.set_author(
            name=f"[{self.client.outfit.alias}] {self.client.outfit.name}", 
            icon_url="https://www.outfit-tracker.com/usercontent/outfits/logo/37573720558810750.png"
        )


class Participant:

    def __init__(self, member, role: str):

        self.member = member
        self.__role = role

    @property
    def role(self) -> str:

        return self.role.upper()


if __name__ == "__main__":

    start_time = "2021-04-25 18:00:00"
    event = Event(name="some event", start_time=start_time)
    print(event.name)
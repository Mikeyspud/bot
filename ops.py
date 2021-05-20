import discord
from member import Member
from database import Database
from constants import Constants

class Ops:

    def __init__(
        self, 
        _id: int, 
        name="BJay Operation", 
        award=8, 
        time="20:00 CET"
    ):

        self._id = _id
        self.name = name
        self.time = time
        self.__embed_id = None
        if int(award) < 0:
            raise self.AwardCannotBeNegative
        self.__award = int(award)
        self.__squads = dict()
        self.add_squad(name="ALPHA")

    def __str__(self):

        message = f"""
        Name: {self.name}
        ID: {self._id}
        Award: {self.award}
        """
        for squad in self.squads:
            message += str(squad)
        return message

    def __eq__(self, other):

        return self._id == other._id

    def __hash__(self):

        return hash(self._id)

    @property
    def squads(self):

        return self.__squads

    @property
    def award(self):

        return self.__award

    @award.setter
    def award(self, amount):

        if int(amount) < 0:
            raise self.AwardCannotBeNegative
        self.__award = int(amount)

    def add_squad(self, **kwargs):

        self.squads[kwargs["name"]] = (Squad(**kwargs))

    def embed(self):

        embed = discord.Embed(
            title="BJay Signup Bot",
            description=f"Event **{self.name}**",
            color=0x2117db
        )
        embed.set_author(
            name="Get Off My Base Peasants",
            url=Constants.outfit_url(),
            icon_url=Constants.outfit_icon()
        )
        embed.add_field(
            name="Participation Award",
            value=self.award
        )
        return embed

    def squad(self, name: str):

        try:
            return self.squads[name]
        except KeyError:
            raise self.SquadDoesntExist

    def close(self):

        for squad in self.squads:
            for member in squad:
                member.award(points=self.award)

    class SquadDoesntExist(Exception):

        pass

    class AwardCannotBeNegative(Exception):

        pass
        

class Squad:

    UNRESTRICTED_KEY = "Unrestricted"

    def __init__(
        self,
        name: str, 
        squad_lead="No Squad Lead",
        fireteam_lead="No Fireteam Lead",
        max_capacity=12,
    ):

        self.name = name
        self.__embed_id = None
        self._squad_lead = squad_lead
        self._fireteam_lead = fireteam_lead
        self._max_composition = dict()
        self.composition = dict()
        self._max_capacity = max_capacity

    def __str__(self):

        message = f"""
        Name: {self.name}
        ID: {self.__embed_id}
        Composition: {self.composition}
        Max Composition: {self.max_composition}
        """

        return message

    @property
    def squad_lead(self):

        return vars(self).get("_squad_lead")

    @squad_lead.setter
    def squad_lead(self, member: Member, role: str):

        self.add_member(member=member, role=role)
        self._squad_lead = member

    @property
    def fireteam_lead(self):

        return vars(self).get("_fireteam_lead")

    @fireteam_lead.setter
    def fireteam_lead(self, member: Member, role: str):

        self.add_member(member=Member, role=role)
        self._fireteam_lead = member

    @property
    def member_count(self):

        return sum([len(value) for value in self.composition.values()])

    @property
    def max_capacity(self):

        if self.UNRESTRICTED_KEY not in self.max_composition:
            self._max_capacity = sum([value for value in self.max_composition.values()])
        return self._max_capacity

    @max_capacity.setter
    def max_capacity(self, capacity: int):

        if self.UNRESTRICTED_KEY not in self.max_composition:
            raise self.CompositionCapacityConflict
        
        self._max_capacity = capacity
            
    @property
    def max_composition(self) -> dict:

        if len(self._max_composition) == 0:
            self._max_composition = {self.UNRESTRICTED_KEY: self.member_count}
        
        return self._max_composition

    @max_composition.setter
    def max_composition(self, composition_list: list):

        if len(composition_list) % 2 != 0:
            raise self.InvalidComposition
        elif len(composition_list) == 0:
            self._max_composition = {self.UNRESTRICTED_KEY: self.member_count}
            return

        self._max_composition = dict()
        self.composition = dict()
        for i in range(0, len(composition_list)-1, 2):
            role = composition_list[i]
            try:
                count = int(composition_list[i+1])
            except ValueError:
                raise self.InvalidComposition
            self._max_composition[role] = count

    def remove_member(self, member: Member):

        [self.composition[r].discard(member) for r in self.composition]

    def add_member(self, member: Member, role: str):

        if self.member_count == self.max_capacity:
            raise self.MaxCapacity

        if self.UNRESTRICTED_KEY not in self.max_composition and role not in self.max_composition:
            raise self.InvalidRole

        self.remove_member(member=member)
        self.composition[role] = {member}.union(self.composition.get(role, set()))

    def embed(self):

        embed = discord.Embed(
            title="BJay Signup Bot",
            description=f"Event {self.name}",
            color=0xebc20a
        )
        embed.set_author(
            name="Get Off My Base Peasants",
            url=Constants.outfit_url(),
            icon_url=Constants.outfit_icon()
        )
        if self.squad_lead:
            embed.add_field(name="Squad Leader", value=self.squad_lead.embed_string__)
        if self.fireteam_lead:
            embed.add_field(name="Fireteam Leader", value=self.fireteam_lead.embed_string__)
        for role in self.composition:
            member_list = str()
            for member in self.composition[role]:
                member_list += f"{member.embed_string__}\n"
            role_string = f"{role.capitalize()}: {len(self.composition[role])}/{self.max_composition.get(role, '-')}"
            embed.add_field(name=role_string, value=member_list, inline=False)

                

        return embed
        
    class MaxCapacity(Exception):

        pass

    class InvalidComposition(Exception):

        pass

    class CompositionCapacityConflict(Exception):

        pass

    class InvalidRole(Exception):

        pass

from event import Event

class Constants:

    @classmethod
    def member_identifier(cls) -> int:

        return 828872958692294708

    @classmethod
    def outfit_identifier(cls) -> str:

        return "37573720558810750"

    @classmethod
    def faction_identifier(cls) -> str:

        return "2"

    @classmethod
    def event(cls) -> Event:

        return Event

    @classmethod
    def outfit_icon(cls) -> str:

        return "https://www.outfit-tracker.com/usercontent/outfits/logo/37573720558810750.png"

if __name__ == "__main__":

    print(Constants.member_identifier())
from urllib3 import PoolManager
from re import search as re_search
from csv import reader as csv_reader

DATA_KEYS = ['名称', '都道府県', '無線局の目的', '免許の年月日']

class Station():
    def __init__(
        self,
        name,
        location,
        purpose,
        expiry_date
    ):
        self.name = name
        self.location = location
        self.purpose = purpose,
        self.expiry_date = expiry_date
        self.callsign = re_search(
            "[A-Z,0-9]+",
            self.name
        )[0]

    def into_json(self):
        return {
            self.callsign: {
                "name": self.name,
                "location": self.location,
                "purpose": self.purpose,
                "expiry_date": self.expiry_date,
            }
        }

def search(
    type,
    callsign=None,
    prefecture=None,
    freq_from=None,
    freq_to=None,
    owner_name=None
):
    raw_datas = PoolManager().request(
        "GET",
        "https://www.tele.soumu.go.jp/musen/SearchServlet?MA={callsign}&SelectID=1&SelectOW=0{type}&HC={prefecture}&FF={freq_from}&TF={freq_to}&NA={owner_name}&DC=100&SK=2&pageID=5&SC=1&CONFIRM=1".format(
            callsign=callsign,
            type=type,
            prefecture=prefecture,
            freq_from=freq_from,
            freq_to=freq_to,
            owner_name=owner_name
        )
    ).data.decode("shift-jis")

    result = [
        line for line in csv_reader(
            raw_datas.splitlines()
        )
        if line != []
    ]

    result = result[
        # get index of ['名称', '都道府県', '無線局の目的', '免許の年月日'] . Lists after that will be the results we're looking for.
        result.index(DATA_KEYS) + 1:
    ]

    return [
        Station(*station_data) for station_data in result
    ]


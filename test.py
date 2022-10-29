from mis import search
from constants import (
    AMATEUR,
    TOKYO
)

if __name__ == "__main__":
    for station in search(
        AMATEUR,
        "JA1Y",
        TOKYO
    ):
        print(station.callsign)
import urllib3

http = urllib3.PoolManager()

def _readReturnFile(filename):
    with open(filename, "r") as f:
        return f.read()

def searchByCallsign(callsign, use_cache=False):
    theUrl = "https://www.tele.soumu.go.jp/musen/SearchServlet?MA={}&SelectID=1&SelectOW=01&DC=100&SK=2&pageID=5&SC=1&CONFIRM=1".format(callsign)
    data = http.request("GET",theUrl).data.decode("shift-jis") if not use_cache else _readReturnFile("cache")
    with open("cache", "w") as f:
        f.write(data)
    data = data.splitlines()

    desalinate = lambda str: str.replace('"', '').split(",")
    theDatas = data[8:]
    theFormat = desalinate(data[7])
    result = []
    for theData in theDatas:
        theData = desalinate(theData)
        packed = {theFormat: theData for theFormat, theData in zip(theFormat, theData) }
        result.append(packed)

    return result

print(searchByCallsign("JA1ZG",use_cache=False))
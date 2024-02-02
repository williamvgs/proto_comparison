def readvalue():
    import json
    file = open("Thrusters.json")
    data = json.load(file)
    azimuth, tunnel, db = 0, 0, 0
    for i in data['thrusters']["azimuth"]:
        azimuth += 1
    for i in data["thrusters"]["tunnel"]:
        tunnel += 1
        if data["thrusters"]["tunnel"][i]["connected_to"] != "none":
            db += 1
    return [0, azimuth], [0, tunnel], [0, int(db/2)], [0, "Max:1"]

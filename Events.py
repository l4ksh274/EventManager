import datetime
import json
import time


class Events:

    def __init__(self):
        self.events = self.getEventList()

    def update(self):
        self.events = self.getEventList()

    def getEventList(self):
        try:
            with open('events.json', 'r') as x:
                return json.load(x)
        except json.JSONDecodeError:
            return None

    def checkAvailable(self, dateTime):
        dates = [i["date"] for i in self.events["Events"]]
        if self.events is None or dateTime not in dates:
            return True
        else:
            return False

    def regEvent(self, name, dateTime):
        if self.checkAvailable(dateTime):
            with open('events.json', 'w') as file:
                self.events["Events"].append({"name": name, "date": dateTime, "id": name.upper() + "_" + dateTime})
                json.dump(self.events, file, indent=4)
        self.update()

    def delEvent(self, eventID):
        events = self.events
        for i in events['Events']:
            if i['id'] == eventID:
                del events['Events'][events['Events'].index(i)]
                break

        with open('events.json', 'w') as file:
            json.dump(self.events, file, indent=4)
        self.update()

    def checkEvent(self, eventID):
        eventDateTime = datetime.datetime.timestamp(
            datetime.datetime.strptime(eventID.split("_")[-1], '%Y-%m-%d %H:%M'))
        cDateTime = time.time()
        if eventDateTime > cDateTime:
            return True
        else:
            return False

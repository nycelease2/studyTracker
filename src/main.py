#!/bin/python

import datetime
from pathlib import Path
import json

f1 = "%Y-%m-%dT%H:%M:%S"


class SessionManager:
    def __init__(self, data_file):
        self.data_file = Path(data_file)

    def load(self):

        if self.data_file.exists():
            session_data_file = open(self.data_file, "r")
        else:
            f = open("sessions.json", "w")
            f.write("[]")
            f.close()
            session_data_file = open(self.data_file, "r")

        self.session_data = json.load(session_data_file)
        session_data_file.close()

        return self.session_data

    def save(self):
        session_data_file = open(self.data_file, "w")
        json.dump(self.session_data, session_data_file, indent=4)
        session_data_file.close()


    def add(self, obj):
        self.session_data.append(obj.to_dict)

    def from_dict(self, dictionary):
        sessionOBJ = Session(dictionary.get("start_time"), dictionary.get("end_time"), dictionary.get("title"), dictionary.get("description"))
        return sessionOBJ



class Session:
    def __init__(self, start_time, end_time, topic, desc):
        self.start_datetime = datetime.datetime.strptime(start_time, f1)
        self.end_datetime = datetime.datetime.strptime(end_time, f1)

        self.total_time = self.end_datetime - self.start_datetime

        self.topic = topic
        self.desc = desc

    def to_dict(self):
         dict = {
                    "title": self.topic,
                    "description": self.desc,
                    "start_time": self.start_datetime.isoformat(),
                    "end_time": self.end_datetime.isoformat()

                 }
        
         return dict
        


def main():
    topic = input("topic: ")
    start_time = input("start time (YYYY-MM-DDTHH:MM:SS): ")
    end_time = input("end time (YYYY-MM-DDTHH:MM:SS): ")
    desc = input("description: ")

    sessionOBJ = Session(start_time, end_time, topic, desc)

    manager = SessionManager("sessions.json")
    manager.add(sessionOBJ)

if __name__=="__main__":
   main()

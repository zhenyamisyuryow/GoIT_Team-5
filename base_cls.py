from collections import UserDict
import re
from datetime import datetime
import pickle

class Field:
    pass


class Name(Field):
    pass

class Phone(Field):
    pass


class Email(Field):
    pass


class Birthday(Field):
    pass


class Address(Field):
    pass


class Note(UserDict):
    pass


class Contacts(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def get_record(self, name):
        return self.data.get(name)

    def delete_record(self, name):
        return self.data.pop(name, None)

    def iterator(self, num_records):
        records = list(self.data.values())
        for i in range(0, len(records), num_records):
            yield records[i:i + num_records]
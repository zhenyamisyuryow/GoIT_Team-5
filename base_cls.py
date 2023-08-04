from collections import UserDict
import re
from datetime import datetime
import pickle

class Field:
    pass


class Name(Field):
    pass

class Phone(Field):
    def __init__(self, phone):
        self.__value = None
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        try:
            pattern = r"\+?3?8?[- (]?0\d{2}[- )]?\d{3}[- ]?\d{2}[- ]?\d{2}$"
            add_cod = "+380"
            result = (re.search(pattern, phone)).group()
            res_phone = re.sub(r"(\D)", "", result)
            form_phone = add_cod[0:13-len(res_phone)] + res_phone
            self.__value = form_phone

        except AttributeError:
            print(f"Вводите корректно номера телефонов, например, в формате: \033[34m0XX-XXX-XX-XX\033[0m")



class Email(Field):
    pass


class Birthday(Field):
    pass


class Address(Field):
    pass

class Record:
    pass

class Note(UserDict):
    pass


class Contacts(UserDict):
    pass
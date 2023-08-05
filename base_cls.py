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
        result = re.findall(r"\+380{1}[(]{1}\d{2}[)]{1}[-]{1}\d{3}[-]{1}\d{2}[-]{1}\d{2}", phone)
        if not result:
            raise ValueError(f"Please enter correct phone numbers in the format: +380(XX)-XXX-XX-XX")
        
        self.__value= "+"+re.sub(r"(\D)","",result[0])
        
        




class Email(Field):
    pass


class Birthday(Field):
    def __init__(self, value : str = None):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        try:
            result = re.findall(r"\d\d-\d\d-\d{4}", value)
            res_data = datetime.strptime(result[0], '%d-%m-%Y')
            if res_data <= datetime.now():
                self.__value = res_data.date()
            else:
                print(f"Date of birth cannot be in the future! Please try again")
        except ValueError:

            print(f"Please enter correct data in the format: \033[34mmm-dd-yyyy\033[0m")
    
    def __str__(self) -> str:
        try:
            return f"date of birth: \033[34m{self.value.strftime('%d-%m-%y')}\033[0m"

        except AttributeError:
            return ""

    


class Address(Field):
    pass

class Record:
    pass

class Note(UserDict):
    pass


class Contacts(UserDict):
    pass


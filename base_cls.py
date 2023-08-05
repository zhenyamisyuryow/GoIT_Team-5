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
    def __init__(self, value : str = None):
        self.__value = None
        self.value = value

    @property
    def value(self):
        if self.__value < datetime.now().date():
            return self.__value


    @value.setter
    def value(self, value):
        try:
            birth_date = re.findall('\d+', value)
            if birth_date[2] and len(birth_date[2])==4:
                birth_date[2] = birth_date[2][2:]
            birth ="/".join(birth_date)
            self.__value = datetime.strptime(birth, '%d/%m/%y').date()
        except ValueError:

            print(f"Введите корректную дату в формате \033[34mmm-dd-yyyy\033[0m")
    
    def __str__(self) -> str:
        try:
            return f"дата рождения: \033[34m{self.value.strftime('%d-%m-%y')}\033[0m"

        except AttributeError:
            return ""

    


class Address(Field):
    pass

class Record:
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
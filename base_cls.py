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
    def __init__(self, email):
        self.__value = None
        self.value = email
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, email):
        if re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.__value = email
        else:
            raise ValueError("Email should match the format johndoe@domain.com")


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
    def __init__(self, name, phone=None, birthday=None, email=None, address=None):
        self.name = name
        self.phones = []
        if phone:
            self.add_phone(phone)
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None
        self.address = Address(address) if address else None

    def add_phone(self, phone):             #Добавить номер телефона
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):         #Изменить номер телефона
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone

    def delete_phone(self, phone):          #Удалить номер телефона
        self.phones.remove(phone)

    def add_birthday(self, birthday):           #Добавить даты рождения
        self.birthday = Birthday(birthday)

    def edit_birthday(self, birthday):      #Изменить дату рождения
        if self.birthday:
            self.birthday.value = birthday
        else:
            self.birthday = Birthday(birthday)

    def add_email(self, email):         #Добавить почту
        self.email = Email(email)

    def edit_email(self, email):        #Изменить почту
        if self.email:
            self.email.value = email
        else:
            self.email = Email(email)

    def add_address(self, address):         #Добавить домашний адрес
        self.address = Address(address)

    def edit_address(self, address):            #Изменить домашний адрес
        if self.address:
            self.address.value = address
        else:
            self.address = Address(address)

    def __repr__(self):             #Вывести все поля для класса Record в строку
        return f"Record(name='{self.name}', phones={self.phones}, birthday={self.birthday}, email={self.email}, address={self.address})"

class Note(UserDict):
    pass


class Contacts(UserDict):
   
    def add_record(self, record: Record):       #Добавление записи
        self.data[record.name.value] = record

    def get_record(self, name):     #Вывод записи
        return self.data.get(name)

    def delete_record(self, name):      #Удаление записи
        return self.data.pop(name, None)

    def iterator(self, num_records):        #Итератор(Принимает число, возвращает генератор)
        records = list(self.data.values())
        for i in range(0, len(records), num_records):
            yield records[i:i + num_records]

    def search_contacts(self, query):
        contacts = []
        for record in self.data.values():
            if query.lower() in str(record.name).lower():
                contacts.append(record)
            else:
                for phone in record.phones:
                    if query in phone.value:
                        contacts.append(record)
                        break
        return contacts
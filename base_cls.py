from collections import UserDict
import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other) -> bool:
        return self.value == other.value
    


class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, phone):
        result = re.findall(r"\+380{1}[(]{1}\d{2}[)]{1}[-]{1}\d{3}[-]{1}\d{2}[-]{1}\d{2}", phone)
        if not result:
            raise ValueError(f"{Colors.FAIL}{Colors.UNDERLINE}Please enter correct phone numbers in the format: +380(XX)-XXX-XX-XX{Colors.ENDC}")
        
        self._value= "+"+re.sub(r"(\D)","",result[0])
        



class Email(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, email):
        if re.match(r'^[a-z0-9]+[._\-+]*[a-z0-9]*@\w+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$', email):
            self._value = email
        else:
            raise ValueError("Email should match the format johndoe@domain.com")


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, value):
        try:
            result = re.findall(r"\d\d-\d\d-\d{4}", value)
            res_data = datetime.strptime(result[0], '%d-%m-%Y')
            if res_data <= datetime.now():
                self._value = res_data.date()
            else:
                print(f"Date of birth cannot be in the future! Please try again")
        except:
            raise ValueError(f"Please enter correct data in the format: \033[34mmm-dd-yyyy\033[0m")
    
    def __str__(self) -> str:
        try:
            return f"date of birth: \033[34m{self.value.strftime('%d-%m-%y')}\033[0m"

        except AttributeError:
            return ""

    def __calc_birthday__(self):
        today = datetime.now().date()
        birth_date = self.value
        if birth_date.month == 2 and birth_date.day == 29:
            future_birthday = datetime(year = today.year, month = 2, day = birth_date.day - int(bool(today.year%4))).date()
            
            if future_birthday < today: 
                future_birthday = datetime(year = today.year + 1, month = 2, day = birth_date.day - int(bool((today.year+1)%4))).date()
            
        else:
            future_birthday = datetime(year = today.year, month = birth_date.month, day = birth_date.day).date()
            if future_birthday < today:
                future_birthday = future_birthday.replace(year = today.year + 1)
        return (future_birthday - today).days


class Address(Field):
    pass

class Record:
    def __init__(self, name, phone=None, birthday=None, email=None, address=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.add_phone(phone)
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None
        self.address = Address(address) if address else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = Phone(new_phone)


    def delete_phone(self, phone : Phone):
            
        try:   
            self.phones.remove(phone)
            return f"Phone {phone} was successfully deleted!"
        except ValueError:
            return f"There is no such number: {phone} in the contact list!"
        

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def edit_birthday(self, birthday):
        if self.birthday:
            self.birthday.value = birthday
        else:
            self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, email):
        if self.email:
            self.email.value = email
        else:
            self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, address):
        if self.address:
            self.address.value = address
        else:
            self.address = Address(address)

    def __iter__(self):
        self._iter_index = 0
        self._fields = [
            self.name,
            *self.phones,
            self.birthday,
            self.email,
            self.address
        ]
        return self

    def __next__(self):
        if self._iter_index < len(self._fields):
            value = self._fields[self._iter_index]
            self._iter_index += 1
            return value
        else:
            raise StopIteration

    def __repr__(self):             #Вывести все поля для класса Record в строку
        return f"Name: {self.name},\nPhones: {self.phones},\nEmail: {self.email},\nBirthday: {self.birthday},\nAddress: {self.address}"


class Note():
    def __init__(self, title: str = None, content: str = None, tags: list = None):
        self.title = title
        self.content = content
        self.tags = tags

    def add_title(self, title: str):
        self.title = title

    def add_content(self, content: str):
        self.content = content

    def add_tags(self, tags: list):
        if tags:
            self.tags.extend(tags)

    
    def edit_title(self, title: str):
        self.title = title

    
    def edit_content(self, content: str):
        self.content = content

    
    def edit_tags(self, tags: list):
        self.tags = tags

    

    def __repr__(self) -> str:
        return f"Note(title='{self.title}', content='{self.content}', tags={self.tags})"

class Notes(Note):
  
    def __init__(self):
        self.data = {}
        
        
    def add_note(self, name: str, title: str = None, content: str = None, tags: list = None):
        note = Note(title, content, tags)
        self.data[name] = note


    def __str__(self) -> str:
        return f"Title: {self.title},\nContent: {self.content},\nTags: {self.tags}"

    
    def get_note(self, title: str):
        return self.data.get(title)


    def delete_note(self, name: str):
        try:
            self.data.pop(name)
            return(f"Note {name} was successfully deleted from the notes ")
        except KeyError:
            return f"There is no such note: {name} in the notes!"



class Contacts(UserDict):
    
   
    def add_record(self, record: Record):       #Добавление записи
        self.data[record.name.value] = record

    def get_record(self, name):     #Вывод записи
        return self.data.get(name)

    def delete_record(self, name):      #Удаление записи
        try:
            self.data.pop(name)
            return(f"Contact {name} was successfully deleted from the book ")
        except KeyError:
            return f"There is no such contact: {name} in the book!"

    def iterator(self, num_records):        #Итератор(Принимает число, возвращает генератор)
        records = list(self.data.values())
        for i in range(0, len(records), num_records):
            yield records[i:i + num_records]

    def search_contacts(self, query):           #Функционал поиска в контактной книге
        contacts = []
        for record in self.data.values():
            if query.lower() in str(record.name).lower():
                contacts.append(str(record))
            else:
                for phone in record.phones:
                    if query in phone.value:
                        contacts.append(str(record))
                        break
        return '\n\n'.join(contacts)
    
    def congratulate_period(self, number_days):
        start_period = datetime.now().date()
        end_period = start_period + timedelta(number_days)
        list_congratulate = []
        for record in self.data.values():
            if record.birthday:
                if record.birthday.__calc_birthday__() <= number_days:
                    list_congratulate.append(record)
        if list_congratulate:
            nl = '\n\n'
            return f"{Colors.OKGREEN}For the period from {start_period} to {end_period}, the following contacts have birthdays in {number_days} days:{Colors.ENDC}\n{f'{nl}'.join(str(p) for p in list_congratulate)}"
        else:
            return f"For the period from {start_period} to {end_period}, there are no birthdays recorded in your book"
        
    
        
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




        





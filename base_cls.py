from collections import UserDict
import re
from datetime import datetime, timedelta
import pickle

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
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone

    def delete_phone(self, phone):
        self.phones.remove(phone)

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

    def add_tags(self, tags_str: str):
        tags_list = tags_str.split(",") # Convert the input string to a list of tags
        self.tags.extend(tags_list)

    
    def edit_title(self, title: str):
        self.title = title

    
    def edit_content(self, content: str):
        self.content = content

    
    def edit_tags(self, tags: list):
        self.tags = tags

    
    def __str__(self) -> str:
        return f"Title: {self.title},\nContent: {self.content},\nTags: {self.tags}"

class Notes(UserDict):
    
    def add_note(self, note:Note):
        self.data[note.title] = note
    
    def get_note(self, title: str):
        return self.data.get(title)

    def delete_note(self, title: str):
        return self.data.pop(title, None)
    
    def search_note(self, query: str):
        notes_results = []        
        for key, value in self.data.items():
            if str(value).lower().find(query.lower()) != -1:
                notes_results.append(value)
        return notes_results
    
    def sort_by_tag(self):
        sorted_notes = sorted(self.data.values(), key=lambda note: note.tags[0] if note.tags else "")
        self.data = {note.title: note for note in sorted_notes}
        return sorted_notes


class Contacts(UserDict):
    
    filename = "data.bin"
   
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
        
    def load_book(self):

        try:
            with open(self.filename, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            pass
    
    def save_book(self):
        with open(self.filename, "wb") as fh:
            pickle.dump(self.data, fh)   
    
        
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
    
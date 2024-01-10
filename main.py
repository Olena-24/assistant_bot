from datetime import datetime
from collections import UserDict
import re
import json

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Phone number must have 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError("Birthday must be in YYYY-MM-DD format")
        super().__init__(value)

class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) if isinstance(phone, str) else phone for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if isinstance(birthday, str) else birthday

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Phone number not found")

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone number not found")

    def days_to_birthday(self):
        if self.birthday:
            now = datetime.now()
            b_date = datetime.strptime(self.birthday.value, '%Y-%m-%d')
            next_birthday = b_date.replace(year=now.year)
            if next_birthday < now:
                next_birthday = next_birthday.replace(year=now.year + 1)
            return (next_birthday - now).days
        else:
            return None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        bday_str = f', birthday: {self.birthday.value}' if self.birthday else ''
        return f"Contact name: {self.name.value}, phones: {phones_str}{bday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, query):
        for record in self.data.values():
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                return record
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def save(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.data, file, default=lambda obj: obj.__dict__, indent=4)

    def load(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            for name, record in data.items():
                phones = [Phone(p['value']) for p in record['phones']]
                birthday = Birthday(record['birthday']['value']) if record['birthday'] else None
                self.add_record(Record(name, phones, birthday))

# Приклад використання
address_book = AddressBook()
address_book.add_record(Record("John Doe", ["1234567890"], "1990-01-01"))
address_book.add_record(Record("Jane Smith", ["0987654321"]))

# Збереження адресної книги
address_book.save("address_book.json")

# Завантаження адресної книги
loaded_book = AddressBook()
loaded_book.load("address_book.json")

# Пошук у книзі контактів
search_result = loaded_book.find("John")
if search_result:
    print(search_result)
else:
    print("No records found.")
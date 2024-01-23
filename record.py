from field import Name, Phone, Email, Address, Birthday
from datetime import date

class Record:
    def __init__(self, name: str, phones=[], email=None, address=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]
        self.email = Email(email) if email else None
        self.address = Address(address) if address else None
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = next((p for p in self.phones if p.value == phone), None)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone not found")

    def edit_phone(self, new_phone):
        for phone in self.phones:
            phone.value = new_phone
        return True

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = date.today()
        next_birthday = self.birthday.value.replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones_str = ", ".join([phone.value for phone in self.phones])
        return f"Name: {self.name.value}, Phones: {phones_str}, Email: {self.email.value if self.email else 'None'}, Address: {self.address.value if self.address else 'None'}, Birthday: {self.birthday.value if self.birthday else 'None'}"

import re
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

class Name(Field):
    pass

class Address(Field):
    pass

class Email(Field):
    @Field.value.setter
    def value(self, value):
        pattern = r"^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.search(pattern, value):
            raise ValueError('Invalid email format.')
        self._value = value

class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, '%Y.%m.%d').date()
        except ValueError:
            raise ValueError('Invalid date format. Correct format: YYYY.MM.DD')

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError('The phone number should be digits only and have 10 symbols.')
        self._value = value

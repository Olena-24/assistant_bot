from collections import UserDict
from record import Record, Phone, Birthday
from serialization import JsonSerializer, PickleSerializer
import pickle

class AddressBook(UserDict):
    def __init__(self, serializer=PickleSerializer()):
        super().__init__()
        self.serializer = serializer
        self.file = 'Phone_Book.bin' if isinstance(serializer, PickleSerializer) else 'Phone_Book.json'

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data:
            # print(self.data[name])
            return self.data[name]
        return None

    def search(self, value: str):
        if len(value) < 3:
            return '\033[91mYou need at least 3 letters to search by name or 3 didgit to search by phone number.\033[0m'
        result = ''
        for name, rec in self.data.items():
            if value.lower() in name.lower():
                result += f'{str(rec)}\n'
            for item in rec.phones:
                if value in item.value:
                    result += f'{str(rec)}'
        if len(result) != 0:
            return result
        else:
            return None

    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)
            return f'The contact {name} has been deleted.'
        else:
            return f'The contact {name} not found.'

    def iterator(self, item_number):
        counter = 0
        result = f'Contacts:\n'
        print(result)
        print(self.data)
        for item, record in self.data.items():
            result += f'{item}: {str(record)}\n'
            counter += 1
            print(counter)
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        print(result)
        yield result

    def write_to_file(self):
        with open(self.file, 'wb') as file:
            pickle.dump(self.data, file)

    def read_from_file(self):
        with open(self.file, 'rb') as file:
            self.data = pickle.load(file)
        return self.data


    def write_to_file(self):
        with open(self.file, 'wb') as file:
            pickle.dump(self.data, file)

    def read_from_file(self):
        with open(self.file, 'rb') as file:
            self.data = pickle.load(file)
        return self.data

   def save(self):
       self.serializer.serialize(self.data, self.file)

    def load(self):
        self.data = self.serializer.deserialize(self.file)
        for name, rec in self.data.items():
            phones = [Phone(p['value']) for p in rec['phones']]
            birthday = Birthday(rec['birthday']['value']) if rec.get('birthday') else None
            self.data[name] = Record(name, phones, birthday)

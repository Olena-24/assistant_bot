from collections import UserDict
from record import Record, Phone, Birthday
from serialization import JsonSerializer, PickleSerializer

class AddressBook(UserDict):
    def __init__(self, serializer=PickleSerializer()):
        super().__init__()
        self.serializer = serializer
        self.file = 'Phone_Book.bin' if isinstance(serializer, PickleSerializer) else 'Phone_Book.json'

    def save(self):
        self.serializer.serialize(self.data, self.file)

    def load(self):
        self.data = self.serializer.deserialize(self.file)
        for name, rec in self.data.items():
            phones = [Phone(p['value']) for p in rec['phones']]
            birthday = Birthday(rec['birthday']['value']) if rec.get('birthday') else None
            self.data[name] = Record(name, phones, birthday)


    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name, None)

    def search(self, value: str) -> str:
        if len(value) < 3:
            return 'You need at least 3 letters to search by name or 3 digits to search by phone number.'
        results = []
        for name, rec in self.data.items():
            if value.lower() in name.lower() or any(value in phone.value for phone in rec.phones):
                results.append(str(rec))
        return '\n'.join(results) if results else 'No matches found.'

    def delete(self, name: str) -> str:
        if name in self.data:
            del self.data[name]
            return f'The contact {name} has been deleted.'
        else:
            return f'The contact {name} not found.'

    def iterator(self, item_number: int):
        counter = 0
        result = 'Contacts:\n'
        for item, record in self.data.items():
            result += f'{item}: {str(record)}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        yield result
     
   def write_to_file(self):
        self.save()
            
    def read_from_file(self):
        self.load()

from collections import UserDict
from record import Record
from serialization import JsonSerializer, PickleSerializer

class AddressBook(UserDict):
    def __init__(self, serializer=PickleSerializer()):
        super().__init__()
        self.serializer = serializer
        self.file = 'Phone_Book.bin' if isinstance(serializer, PickleSerializer) else 'Phone_Book.json'

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name, None)

    def search(self, query: str) -> str:
        results = []
        for name, record in self.data.items():
            if query.lower() in name.lower() or any(query in phone.value for phone in record.phones):
                results.append(str(record))
        return '\n'.join(results) if results else "No matches found."

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            return f"Contact {name} not found."

    def save(self):
        self.serializer.serialize(self.data, self.file)

    def load(self):
        self.data = self.serializer.deserialize(self.file)

    def iterator(self, number_of_items: int):
        count = 0
        result = ''
        for name, record in self.data.items():
            result += str(record) + '\n'
            count += 1
            if count >= number_of_items:
                yield result
                result = ''
                count = 0
        if result:
            yield result



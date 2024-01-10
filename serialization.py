import json
import pickle
from abc import ABC, abstractmethod

class Serializer(ABC):
    @abstractmethod
    def serialize(self, data, filename):
        pass

    @abstractmethod
    def deserialize(self, filename):
        pass

class JsonSerializer(Serializer):
    def serialize(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, default=lambda obj: obj.__dict__, indent=4)

    def deserialize(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)

class PickleSerializer(Serializer):
    def serialize(self, data, filename):
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    def deserialize(self, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

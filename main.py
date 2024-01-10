from collections import UserDict
import json
from field import Name, Phone, Birthday
from record import Record
from addressbook import AddressBook


# Сохранение адресной книги
address_book.save("address_book.json")

# Загрузка адресной книги
loaded_book = AddressBook()
loaded_book.load("address_book.json")

# Поиск в адресной книге
search_result = loaded_book.find("John")
if search_result:
    print(search_result)
else:
    print("No records found.")

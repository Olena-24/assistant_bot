from addressbook import AddressBook
from record import Record

def main():
    # Инициализация адресной книги
    address_book = AddressBook()

    # Запрос данных у пользователя для добавления записей
    while True:
        name = input("Enter name (or leave empty to stop): ")
        if not name:
            break
        phones = input("Enter phone numbers, separated by commas: ").split(',')
        birthday = input("Enter birthday in YYYY.MM.DD format (or leave empty): ")

        # Создание и добавление записи в адресную книгу
        address_book.add_record(Record(name, phones, birthday))

    # Сохранение адресной книги в файл
    address_book.save("address_book.json")

    # Загрузка адресной книги из файла
    loaded_book = AddressBook()
    loaded_book.load("address_book.json")

    # Поиск в адресной книге
    query = input("Enter a name or phone number to search: ")
    search_result = loaded_book.find(query)
    if search_result:
        print(search_result)
    else:
        print("No records found.")

if __name__ == "__main__":
    main()

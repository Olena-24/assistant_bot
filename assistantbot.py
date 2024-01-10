from rich.console import Console
from addressbook import AddressBook
from record import Record

class AssistantBot:
    def __init__(self):
        self.console = Console()
        self.phone_book = AddressBook()

    def run(self):
        self.console.print("Запуск Assistant Bot")
        while True:
            self.console.print("1: Добавить контакт\n2: Найти контакт\n3: Удалить контакт\n4: Показать все контакты\n5: Выход")
            choice = input("Выберите действие: ")

            if choice == "1":
                self.add_contact()
            elif choice == "2":
                self.find_contact()
            elif choice == "3":
                self.delete_contact()
            elif choice == "4":
                self.show_all_contacts()
            elif choice == "5":
                break
            else:
                self.console.print("Неправильный выбор, попробуйте снова.")

    def add_contact(self):
        name = input("Введите имя: ")
        phone = input("Введите телефон: ")
        email = input("Введите email: ")
        address = input("Введите адрес: ")
        birthday = input("Введите день рождения: ")

        record = Record(name)
        record.add_phone(phone)
        record.add_email(email)
        record.add_address(address)
        record.add_birthday(birthday)

        self.phone_book.add_record(record)
        self.console.print(f"Контакт {name} добавлен.")

    def find_contact(self):
        name = input("Введите имя для поиска: ")
        record = self.phone_book.find(name)
        if record:
            self.console.print(record)
        else:
            self.console.print(f"Контакт {name} не найден.")

    def delete_contact(self):
        name = input("Введите имя для удаления: ")
        if self.phone_book.delete(name):
            self.console.print(f"Контакт {name} удален.")
        else:
            self.console.print(f"Контакт {name} не найден.")

    def show_all_contacts(self):
        for name, record in self.phone_book.items():
            self.console.print(f"{name}: {record}")

if __name__ == "__main__":
    bot = AssistantBot()
    bot.run()

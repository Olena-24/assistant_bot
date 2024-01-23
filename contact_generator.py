import random
import re
from contact_book import AssistantBot, Record, AddressBook
from faker import Faker

fake = Faker('uk_UA')

def generate_name():
    name = fake.name()
    return normalize(name)


assistant_bot = AssistantBot()
AddressBook_bot = AddressBook()

# Создаем переменную с украинским алфавитом
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
# Создаем переменную (список) для транслейта
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "i", "ji", "g")
# Создаем пустой словарь для транслейта
CONVERTS = dict()

# Заполняем словарь
for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    CONVERTS[ord(cyrillic)] = latin
    CONVERTS[ord(cyrillic.upper())] = latin.upper()


# Создаем функцию для чистки от всех лишних символов и преобразовываем и заменя на транслейт
def normalize(name: str) -> str:
    cyrillic_symbols = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "i", "ji", "g")
    converts = dict()

    for cyrillic, latin in zip(cyrillic_symbols, translation):
        converts[ord(cyrillic)] = latin
        converts[ord(cyrillic.upper())] = latin.upper()

    translate_name = re.sub(r'\W', '_', name.translate(converts))
    return translate_name


def generate_phone_number():
    return f"0{random.randint(50, 99)}{random.randint(100, 999)}{random.randint(1000, 9999)}"


def generate_birthdate():
    year = random.randint(1970, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}.{month:02d}.{day:02d}"



def generate_email(name):
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com"])
    return fake.email()


def generate_email(name):
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com"])
    return fake.email()

# Create a function to generate an address
def generate_address():
    cities = ["Kyiv", "Lviv", "Odesa", "Kharkiv", "Dnipro"]
    streets = ["Main St", "First St", "Second St", "Third St", "Park Ave"]
    return f"{random.choice(streets)}, {random.randint(1, 100)}, {random.choice(cities)}"

# Create a function to generate a contact book
def generate_contact_book(num_entries, phone_book):
    for _ in range(num_entries):
        name = generate_name()
        phones = generate_phone_number()
        birthday = generate_birthdate()
        email = generate_email(name)
        address = generate_address()

        record = Record(name)
        record.add_phone(phones)
        record.add_birthday(birthday)
        record.add_email(email)
        record.add_address(address)
        phone_book[name] = record

# Create a function to display generated contacts
def display_contacts(phone_book):
    for name, record in phone_book.items():
        print(f"Name: {name}")
        print(f"Phones: {record.phones}")
        print(f"Birthday: {record.birthday}")
        print(f"Email: {record.email}")
        print(f"Address: {record.address}")
        print()

if __name__ == "__main__":
    num_entries = 20
    assistant_bot = AssistantBot()
    generate_contact_book(num_entries, assistant_bot.phone_book)
    display_contacts(assistant_bot.phone_book)
    assistant_bot.exit()

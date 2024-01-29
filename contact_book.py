from collections import UserDict, defaultdict
import cmd
from datetime import date, datetime, timedelta
import pickle
import os
import re
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.table import Table
from field import Name, Phone, Email, Address, Birthday
from record import Record
from addressbook import AddressBook

new_record = Record("Contact name")

class Controller(cmd.Cmd):
    def exit(self):
        self.book.dump()
        return True
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    return wrapper


class AssistantBot:
    def __init__(self, address_book: AddressBook):
        self.console = Console()
        self.phone_book = address_book
        if os.path.isfile(self.phone_book.file):
            self.phone_book.read_from_file()

    # вывод в таблицу rich       
    def table_print(self, record: Record):
        table = Table(title="Contact Information", style="cyan", title_style="bold magenta", width = 100)
        table.add_column("Name", style="red", justify="center")
        table.add_column("Phones", style="bold blue", justify="center")
        table.add_column("Birthday", style="bold green", justify="center")
        table.add_column("Email", style="bold blue", justify="center")
        table.add_column("Address", style="yellow", justify="center")
        table.add_column("Days to birthday", style="yellow", justify="center")
        phone_str = "\n".join(
            "; ".join(p.value for p in record.phones[i:i + 2]) for i in range(0, len(record.phones), 2))
        # {'; '.join(p.value for p in self.phones)}
        table.add_row(
            str(record.name.value),
            str(phone_str),
            str(record.birthday),
            str(record.email),
            str(record.address),
            str(record.days_to_birthday())
        )
        return table

    # отдельная функция по поиску рекорд, чтобы избежать ошибку с несущестующим контактом 
    @input_error
    def find_record(self):
        print('=' * 150)
        completer = WordCompleter(list(self.phone_book.keys()), ignore_case=True)
        name = prompt('Enter the name of an existing contact=> ', completer=completer)
        record: Record = self.phone_book.find(name)
        if record:
            return record

    # добавление нового контакта
    @input_error
    def add_contact(self):
        name = input('Enter name=> ')
        record = Record(name)
        self.add_phone(record)
        self.add_birthday(record)
        self.add_email(record)
        self.add_address(record)
        self.phone_book.add_record(record)
        contact = self.table_print(record)
        print(f'\033[92mYou have created a new contact:\033[0m')
        self.console.print(contact)
        return

    # добавление номера телефона
    @input_error
    def add_phone(self, record):
        count_phone = 1
        while True:
            try:
                print(
                    f'\033[38;2;10;235;190mPlease enter the Phone Number {count_phone}, or press ENTER to skip.\033[0m')
                phone = input('Enter phone=> ')
                if phone:
                    record.add_phone(phone)
                    self.phone_book.add_record(record)
                    print(f'\033[38;2;10;235;190mThe phone number {phone} has been added.\033[0m')
                    count_phone += 1
                else:
                    return
            except ValueError as e:
                print(e)

    @input_error
    def add_phone_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            self.add_phone(record)
            self.console.print(self.table_print(record))
            return

    # добавление даты дня рождения
    def add_birthday(self, record: Record):
        while True:
            try:
                print(f'\033[38;2;10;235;190mEnter the date of birth or press ENTER to skip.\033[0m')
                birth = input('Enter date of birth. Correct format: YYYY.MM.DD=> ')
                if birth:
                    record.add_birthday(birth)
                    self.phone_book.add_record(record)
                    print(f'\033[38;2;10;235;190mThe date of birth {birth} has been added.\033[0m')
                    return
                else:
                    return
            except ValueError as e:
                print(e)

    @input_error
    def add_birthday_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            elif record.birthday == None:
                self.add_birthday(record)
                self.console.print(self.table_print(record))
                return
            else:
                print('\033[91mThis contact has date of birth.\033[0m')
                return

    # добаваление email  
    @input_error
    def add_email(self, record: Record):
        while True:
            try:
                print(f'\033[38;2;10;235;190mEnter the email or press ENTER to skip.\033[0m')
                email = input('Enter email=> ')
                if email:
                    record.add_email(email)
                    self.phone_book.add_record(record)
                    print(f'\033[38;2;10;235;190mThe email {email} has been added.\033[0m')
                    return
                else:
                    return
            except ValueError as e:
                print(e)

    @input_error
    def add_email_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            elif record.email == None:
                self.add_email(record)
                self.console.print(self.table_print(record))
                return
            else:
                print('\033[91mThis contact has email.\033[0m')
                return

    # добавление адреса   
    @input_error
    def add_address(self, record: Record):
        print(f'\033[38;2;10;235;190mEnter your address or press ENTER to skip.\033[0m')
        address = input('Enter address=> ')
        if address:
            record.add_address(address)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mThe address {address} has been added.\033[0m')
            return
        else:
            return

    @input_error
    def add_address_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found\033[0m')
                return
            elif record.address == None:
                self.add_address(record)
                self.console.print(self.table_print(record))
                return
            else:
                print('\033[91mThis contact has address.\033[0m')
                return

    # изменение телефона
    @input_error
    def edit_phone(self, record: Record):
        old_phone = input('Enter the phone number you want to change=> ')
        new_phone = input('Enter the new phone number=> ')
        result = record.edit_phone(old_phone, new_phone)
        if result is None:
            print(f'\033[91mPhone: {old_phone} not found!\033[0m')
            return
        self.phone_book.add_record(record)
        print(f'\033[38;2;10;235;190mYou changed the contact:\n\033[0m')
        self.console.print(self.table_print(record))
        return

    @input_error
    def edit_phone_menu(self):
        name = input("Enter the contact name: ")
        record = self.phone_book.find(name)

        if record:
            new_phone = input("Enter the new phone number=> ")

            try:
                record.edit_phone(new_phone)
                print(f"The phone number has been updated to {new_phone}.")
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("Contact not found.")

    # изменение email      
    @input_error
    def edit_email(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            self.add_email(record)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mYou changed the contact:\n\033[0m')
            self.console.print(self.table_print(record))
            return

    @input_error
    def edit_address(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            self.add_address(record)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mYou changed the contact:\n\033[0m')
            self.console.print(self.table_print(record))
            return

    # изменение имени
    @input_error
    def edit_name(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            new_name = input('Enter new name=> ')
            if new_name:
                old_name = record.name.value
                self.phone_book.data[new_name] = self.phone_book.data.pop(old_name)
                record.name.value = new_name
                self.phone_book.add_record(record)
                print(f'\033[38;2;10;235;190mName changed successfully from {old_name} to {new_name}.\n\033[0m')
                self.console.print(self.table_print(record))
                return
            else:
                return

    # изменение даты рождения
    @input_error
    def edit_birthday_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            self.console.print(self.table_print(record))
            self.add_birthday(record)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mYou changed the contact:\n\033[0m')
            self.console.print(self.table_print(record))
            return

    # удаление номера
    @input_error
    def delete_phone(self, record: Record):
        phone = input('Enter phone=> ')
        result = record.remove_phone(phone)
        print(f'\033[38;2;10;235;190mThe phone number {phone} was removed.\033[0m')
        return result

    @input_error
    def delete_phone_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            self.console.print(self.table_print(record))
            self.delete_phone(record)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mYou changed the contact:\n.\033[0m')
            self.console.print(self.table_print(record))
            return

    # удаление даты рождения
    @input_error
    def delete_birthday_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            record.birthday = None
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mThe date of birth was removed.\033[0m')
            self.console.print(self.table_print(record))
            return

    # удаление email
    @input_error
    def delete_email_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            record.email = None
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mThe email was removed.\033[0m')
            self.console.print(self.table_print(record))
            return

    # удаление адреса
    @input_error
    def delete_address_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            record.address = None
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mThe address was removed.\033[0m')
            self.console.print(self.table_print(record))
            return
        
    # удаление контакта
    @input_error
    def delete_contact_menu(self):
         while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            self.console.print(self.table_print(record))
            print('\033[91mDo you really want to delete this contact? Please enter the number: 1.YES or press ENTER to skip.\033[0m')
            res = input('Enter your text=>  ').lower()
            if res in ('1', 'yes'):
                self.phone_book.delete(record.name.value)
                print(f'\033[38;2;10;235;190mThe contact {record.name.value} was removed.\033[0m')
                return 
            else:
                return

    # поиск по имени и по совпадениям
    @input_error
    def search(self):
        table = Table(title="Search results", style="cyan", title_style="bold magenta", width=100)
        table.add_column("Name", style="red", justify="center")
        table.add_column("Phones", style="bold blue", justify="center")
        table.add_column("Birthday", style="bold green", justify="center")
        table.add_column("Email", style="bold blue", justify="center")
        table.add_column("Address", style="yellow", justify="center")
        table.add_column("Days to birthday", style="yellow", justify="center")
    
        while True:
            print('=' * 100)
            res = input('Enter at least 3 letters, 3 digits, or a date (YYYY.MM.DD) to search, or press ENTER to exit: ').lower()
            if res:
                result = []
                for name, record in self.phone_book.data.items():
                    name_lower = name.lower()
                    phone_digits = "".join(filter(str.isdigit, "".join(p.value for p in record.phones)))
                    address_lower = str(record.address).lower() if record.address else ""
                    birthday_str = record.birthday.value.strftime('%Y.%m.%d') if record.birthday else ""

                    if res in name_lower or res in phone_digits or res in address_lower or res == birthday_str:
                        result.append(record)

                if result:
                    for record in result:
                        phone_str = "; ".join(p.value for p in record.phones)
                        table.add_row(
                            str(record.name.value),
                            str(phone_str),
                            birthday_str,
                            str(record.email),
                            str(record.address),
                            str(record.days_to_birthday())
                        )
                    self.console.print(table)
                else:
                    print('\033[38;2;10;235;190mNo matches found.\033[0m')
            else:
                break

            

    # работа через интератор
    def show_all(self):
        if not self.phone_book.data:
            print('\033[91mNo contacts.\033[0m')
            return

        while True:
            table = Table(title="Contact Information", style="cyan", title_style="bold magenta", width=100)
            table.add_column("Name", style="red", justify="center")
            table.add_column("Phones", style="bold blue", justify="center")
            table.add_column("Birthday", style="bold green", justify="center")
            table.add_column("Email", style="bold blue", justify="center")
            table.add_column("Address", style="yellow", justify="center")
            table.add_column("Days to birthday", style="yellow", justify="center")

            print('=' * 100)
            print('\033[38;2;10;235;190mEnter how many records to display or press ENTER to skip.\033[0m')
            item_number = input('Enter number=> ')

            if item_number.isdigit():
                item_number = int(item_number)
                iteration_count = 0

                for name, record in self.phone_book.data.items():
                    phone_str = "; ".join(p.value for p in record.phones)
                    birthday_str = record.birthday.value.strftime('%Y.%m.%d') if record.birthday else ""
                    email_str = record.email.value if record.email else ""
                    address_str = record.address.value if record.address else ""

                    table.add_row(
                        str(record.name.value),
                        phone_str,
                        birthday_str,
                        email_str,
                        address_str,
                        str(record.days_to_birthday())
                    )

                    iteration_count += 1

                    if iteration_count >= item_number:
                        self.console.print(table)
                        continue_input = input('Press ENTER to show more or type "exit" to return: ')
                        if continue_input.lower() == 'exit':
                            return
                        else:
                            table = Table(title="Contact Information", style="cyan", title_style="bold magenta", width=100)
                            table.add_column("Name", style="red", justify="center")
                            table.add_column("Phones", style="bold blue", justify="center")
                            table.add_column("Birthday", style="bold green", justify="center")
                            table.add_column("Email", style="bold blue", justify="center")
                            table.add_column("Address", style="yellow", justify="center")
                            table.add_column("Days to birthday", style="yellow", justify="center")
                            iteration_count = 0

                
                if iteration_count > 0:
                    self.console.print(table)

                    break

                elif item_number == "":
                    break
        else:
            print('\033[91mInvalid input. Please enter a number.\033[0m')

    def exit(self):
        self.phone_book.write_to_file()
        return


if __name__ == "__main__":
    pass




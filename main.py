import questionary
from termcolor import colored
import time
from contact_book import AssistantBot
from Note import NotesManager
from weather import anecdotes_ua_menu, anecdotes_en_menu, weather_menu
from file_sorter import sorteds_menu
from task_for_birthday import birthdays_for_date_menu, get_birthdays_per_week_menu, birthday_in_given_days_menu
from rich.console import Console
from rich.table import Table
from addressbook import AddressBook



def start_menu():
    address_book = AddressBook()
    assistant_bot = AssistantBot(address_book)
    notes_manager = NotesManager()

    current_menu_number = 1
    text_colors = 'cyan'
    print(colored('Hello!', text_colors))

    def f_exit():   
        assistant_bot.phone_book.write_to_file()  # Add this line to write the phone book to a file
        assistant_bot.exit()
        print(colored('Goodbye!', text_colors))
        exit()

    # Function definitions
    def f_add():
        print(f'You entered: add')

    # Function stub
    def function_stub():
        pass

    commands_start = {
        'ADD': [f_add, 2, 1, "cyan"],
        'EDIT': [function_stub, 3, 1, "blue"],
        'DELETE': [function_stub, 4, 1, "red"],
        'SEARCH': [assistant_bot.search, 1, 1, "blue"],
        'SHOW ALL': [assistant_bot.show_all, 1, 1, "blue"],
        'NOTE': [function_stub, 5, 1, "bright_cyan"],
        'GOODIES': [function_stub, 6, 1, "green"],
        'EXIT': [f_exit, 2, 1, ""],
    }

    commands_add = {
        'CONTACT': [assistant_bot.add_contact, 1, 1, "cyan"],
        'PHONE': [assistant_bot.add_phone_menu, 1, 1, "blue"],
        'BIRTHDAY': [assistant_bot.add_birthday_menu, 1, 1, "green"],
        'EMAIL': [assistant_bot.add_email_menu, 1, 1, "blue"],
        'ADDRESS': [assistant_bot.add_address_menu, 1, 1, "yellow"],
        'RETURN TO MAIN MENU': [function_stub, 1, 0, ""],
        'EXIT': [f_exit, 0, 0, ""],
    }

    commands_edit = {
        'NAME': [assistant_bot.edit_name, 1, 1, "cyan"],
        'PHONE': [assistant_bot.edit_phone_menu, 1, 1, "blue"],
        'BIRTHDAY': [assistant_bot.edit_birthday_menu, 1, 1, "green"],
        'EMAIL': [assistant_bot.edit_email, 1, 1, "blue"],
        'ADDRESS': [assistant_bot.edit_address, 1, 1, "yellow"],
        'RETURN TO MAIN MENU': [function_stub, 1, 0, ""],
        'EXIT': [f_exit, 0, 0, ""],
    }

    commands_del = {
        'CONTACT': [assistant_bot.delete_contact_menu, 1, 1, "cyan"],
        'PHONE': [assistant_bot.delete_phone_menu, 1, 1, "blue"],
        'BIRTHDAY': [assistant_bot.delete_birthday_menu, 1, 1, "green"],
        'EMAIL': [assistant_bot.delete_email_menu, 1, 1, "blue"],
        'ADDRESS': [assistant_bot.delete_address_menu, 1, 1, "yellow"],
        'RETURN TO MAIN MENU': [function_stub, 1, 0, ""],
        'EXIT': [f_exit, 0, 0, ""],
    }

    commands_note = {
        'ADD NOTE': [notes_manager.note_add_menu, 5, 1, "cyan"],
        'EDIT NOTE': [notes_manager.note_charge_menu, 5, 1, "blue"],
        'DELETE NOTE': [notes_manager.note_delete_menu, 5, 1, "red"],
        'SEARCH NOTE': [notes_manager.note_search_menu, 5, 1, "blue"],
        'SHOW ALL NOTE': [notes_manager.note_show_menu, 5, 1, "blue"],
        'RETURN TO MAIN MENU': [function_stub, 1, 0, ""],
        'EXIT': [f_exit, 2, 1, ""],
    }

    commands_goodies = {
        'FILE SORTING': [sorteds_menu, 6, 1, "cyan"],
        'WEATHER': [weather_menu, 6, 1, "blue"],
        'ANECDOTES': [function_stub, 7, 1, "blue"],
        'BIRTHDAY': [function_stub, 8, 1, "green"],
        'RETURN TO MAIN MENU': [function_stub, 1, 0, ""],
        'EXIT': [f_exit, 2, 1, ""],
    }

    commands_anecdotes = {
        'Українською мовою': [anecdotes_ua_menu, 6, 1, "blue"],
        'English language': [anecdotes_en_menu, 6, 1, "yellow"],
        'RETURN TO MAIN MENU': [function_stub, 1, 0, ""],
        'EXIT': [f_exit, 2, 1, ""],
    }

    commands_birthdays = {
        'FOR THIS DAY': [birthdays_for_date_menu, 8, 1, "blue"],
        'THIS WEEK': [get_birthdays_per_week_menu, 8, 1, "blue"],
        'FOR A FEW DAYS': [birthday_in_given_days_menu, 8, 1, "blue"],
        'RETURN TO MAIN MENU': [function_stub, 1, 0, ""],
        'EXIT': [f_exit, 2, 1, ""],
    }

    def add_menu(commands_menu, commands_text):
        console = Console()
        table = Table(show_header=False, style="cyan")
        table.add_column("", style="bold magenta", width=50, justify="center")  # Empty column for left border

        for option, values in commands_menu.items():
            if values[-1]:
                color = values[-1]
                table.add_column(option, style=color, width=len(option) + 5, justify="center")

        row_values = [f"{commands_text}"]
        row_values.extend(option for option, values in commands_menu.items() if values[-1])
        table.add_row(*row_values)

        console.print(table)

    def display_record(record):
        phones_str = ", ".join([phone.value for phone in record.phones])
        birthday = record.birthday.value if record.birthday else 'None'
        email = record.email.value if record.email else 'None'
        address = record.address.value if record.address else 'None'

        return f"{record.name.value}, {phones_str}, {birthday}, {email}, {address}"

    # Function to get user input
    def get_user_input(commands_menu):
        result = questionary.select('Choose an action:', choices=commands_menu.keys()).ask()
        return result

    # Main input loop
    while True:
        commands_menu = commands_start

        if current_menu_number == 1:
            commands_menu = commands_start
            commands_text = "How can I help you? Please choose:"
            add_menu(commands_menu, commands_text)
        elif current_menu_number == 2:
            commands_menu = commands_add
            commands_text = "What would you like to add? Please choose:"
            add_menu(commands_menu, commands_text)
        elif current_menu_number == 3:
            commands_menu = commands_edit
            commands_text = "What do you want to change? Please choose:"
            add_menu(commands_menu, commands_text)
        elif current_menu_number == 4:
            commands_menu = commands_del
            commands_text = "What do you want to delete? Please choose:"
            add_menu(commands_menu, commands_text)
        elif current_menu_number == 5:
            commands_menu = commands_note
            commands_text = "How can I assist you? Please select an option:"
            add_menu(commands_menu, commands_text)
        elif current_menu_number == 6:
            commands_menu = commands_goodies
            commands_text = "How can I assist you? Please select an option:"
            add_menu(commands_menu, commands_text)
        elif current_menu_number == 7:
            commands_menu = commands_anecdotes
            commands_text = "Choose language. Please choose:"
            add_menu(commands_menu, commands_text)
        elif current_menu_number == 8:
            commands_menu = commands_birthdays
            commands_text = "Choose an option. Please choose:"
            add_menu(commands_menu, commands_text)

        user_input = get_user_input(commands_menu)
        current_menu_number = commands_menu[user_input][1]

        if user_input in commands_menu:
            commands_menu[user_input][0]()
        else:
            print('Please select a team.')

if __name__ == "__main__":
    start_menu()

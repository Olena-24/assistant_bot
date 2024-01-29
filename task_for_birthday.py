from collections import defaultdict
from datetime import date, datetime, timedelta
from rich.console import Console
from rich.table import Table
from addressbook import AddressBook
from record import Record, Phone, Birthday
from contact_book import AssistantBot
import os


address_book = AddressBook()  # Create an instance of AddressBook
assistant_bot = AssistantBot(address_book) 

def birthdays_for_date(day):
    date_obj = datetime.strptime(day, '%Y.%m.%d').date()
    contact_birth = []
    for name, rec in assistant_bot.phone_book.data.items():
        if rec.birthday:
            birth = rec.birthday.value.replace(year=date_obj.year)
            if birth == date_obj:
                contact_birth.append(name)
    return contact_birth

def birthdays_for_date_menu():
    table = Table(title="Birthdays information", style="cyan", title_style="bold magenta", width=100)
    table.add_column("Name", style="red", justify="center")
    today_data_str = datetime.today().date().strftime('%Y.%m.%d')

    if not assistant_bot.phone_book:
        console.print("[red]No contacts.[/red]")
        return

    birth = birthdays_for_date(today_data_str)
    if birth:
        names = " | ".join(birth)
        table.add_row(names)
        console.print(table)
    else:
        console.print("[yellow]No birthdays today.[/yellow]")

def get_birthdays_per_week():
    date_today = date.today()
    birthday_per_week = defaultdict(list)
    for name, rec in assistant_bot.phone_book.data.items():
        if rec.birthday:
            birth = rec.birthday.value.replace(year=date_today.year)
            if birth < date_today - timedelta(days=1):
                birth = birth.replace(year=date_today.year+1)
            day_week = birth.strftime("%A")
            if date_today <= birth <= date_today + timedelta(days=7):
                birthday_per_week[day_week].append(name)
    return birthday_per_week

def get_birthdays_per_week_menu():
    table = Table(title="Birthdays information", style="cyan", title_style="bold magenta", width=100)
    table.add_column("Day of the week", style="red", justify="center")
    table.add_column("Names", style="bold blue", justify="center")

    if not assistant_bot.phone_book:
        console.print("[red]No contacts.[/red]")
        return

    birthdays = get_birthdays_per_week()
    if birthdays:
        for day, names in birthdays.items():
            names_str = ', '.join(names)
            table.add_row(day, names_str)
        console.print(table)
    else:
        console.print("[yellow]No birthdays this week.[/yellow]")

def birthday_in_given_days(days):
    date_today = date.today()
    target_date = date_today + timedelta(days=days)
    contact_birth = []
    for name, rec in assistant_bot.phone_book.data.items():
        if rec.birthday:
            birth = rec.birthday.value.replace(year=date_today.year)
            if birth < date_today:
                birth = birth.replace(year=date_today.year+1)
            if date_today <= birth <= target_date:
                contact_birth.append(f'{name}; {rec.birthday.value}; {(birth - date_today).days}')
    return contact_birth

def birthday_in_given_days_menu():
    table = Table(title="Birthdays information", style="cyan", title_style="bold magenta", width=100)
    table.add_column("Name", style="red", justify="center")
    table.add_column("Date of birth", style="bold blue", justify="center")
    table.add_column("Days to birthday", style="bold blue", justify="center")

    if not assistant_bot.phone_book:
        console.print("[red]No contacts.[/red]")
        return

    while True:
        console.print("[green]Enter the required number of days (no more than one year) or press ENTER to skip.[/green]")
        input_number = input("Enter the number: ")
        if input_number.isdigit():
            days_number = int(input_number)
            if days_number <= 365:
                days_birth = birthday_in_given_days(days_number)
                if days_birth:
                    for elem in days_birth:
                        name, dob, days = elem.split(';')
                        table.add_row(name.strip(), dob.strip(), days.strip())
                    console.print(table)
                    return
            else:
                console.print("[red]Number is greater than one year.[/red]")
        elif not input_number:
            return
        else:
            console.print("[red]Invalid input. Please enter a number.[/red]")

if __name__ == "__main__":
    address_book = AddressBook()  # Create an instance of AddressBook
    assistant_bot = AssistantBot(address_book)

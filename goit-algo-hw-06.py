from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def validate_phone(self, phone):
        return len(phone) == 10 and phone.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        if isinstance(phone, Phone):
            self.phones.append(phone)
        else:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if isinstance(phone, Phone):
            self.phones.remove(phone)
        else:
            self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if old_phone in [p.value for p in self.phones]:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError("Phone number not found")

    def __str__(self):
        return f"Contact name: {self.name}, phones: {', '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise ValueError("Contact not found")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Contact not found")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name and phone please."
    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        new_record = Record(name)
        new_record.add_phone(phone)
        contacts.add_record(new_record)
        return f"Contact {name} with phone number {phone} has been added."
    else:
        return f"Contact {name} already exists."

@input_error
def change_contact(args, contacts):
    name, new_phone = args
    if name in contacts.data:
        record = contacts.find(name)
        record.edit_phone(new_phone)
        return f"Phone number for {name} has been changed to {new_phone}."
    else:
        return f"Contact {name} not found."

@input_error
def show_phone(args, contacts):
    name = args[0]
    if name in contacts.data:
        record = contacts.find(name)
        return f"Phone number for {name} is {record.phones[0]}."
    else:
        return f"Contact {name} not found."

@input_error
def show_all_contacts(args, contacts):
    if not contacts:
        return "Phone book is empty."
    else:
        return "\n".join([str(record) for record in contacts.data.values()])

@input_error
def search_contact(args, contacts):
    name = args[0]
    if name in contacts.data:
        record = contacts.find(name)
        return f"Phone number for {name} is {record.phones[0]}."
    else:
        return f"No contact with the name {name} found."

@input_error
def parse_input(input_str):
    tokens = input_str.strip().split()
    command = tokens[0].lower()
    args = tokens[1:]
    return command, args

def show_commands():
    return "Available commands:\n" \
           "add <name> <phone_number>: Add a new contact with the given name and phone number.\n" \
           "change <name> <new_phone_number>: Change the phone number for the contact with the given name.\n" \
           "phone <name>: Show the phone number for the contact with the given name.\n" \
           "search <name>: Search for a contact by name.\n" \
           "all: Show all contacts.\n" \
           "close or exit: Exit the program."

def main():
    phone_book = AddressBook()
    while True:
        user_input = input("Enter command: ")
        command, args = parse_input(user_input)
        if command == "add":
            print(add_contact(args, phone_book))
        elif command == "change":
            print(change_contact(args, phone_book))
        elif command == "phone":
            print(show_phone(args, phone_book))
        elif command == "search":
            print(search_contact(args, phone_book))
        elif command == "all":
            print(show_all_contacts(args, phone_book))
        elif command == "commands":
            print(show_commands())
        elif command == "exit" or command == "close":
            print("Goodbye!")
            break
        else:
            print("Invalid command. Type 'commands' for a list of available commands.")

if __name__ == "__main__":
    main()


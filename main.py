from base_cls import *


contacts = Contacts()


def input_error(func):
    def handler(*args):
        argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
        try:
            return func(*args)
        except KeyError:
            return "Error: key doesn't exist."
        except ValueError as e:
            return e
        except IndexError:
            return "Error: provide both name and phone number."
        except TypeError:
            return f"Error: required parameters are: {', '.join(argnames)}"
    return handler


def hello():
    return "Hello!"

def bye():
    return "Good bye!"

@input_error
def showall():
    number = int(input("How many records would you like to retrieve in one iteration?\n>>> "))
    result = contacts.iterator(number)
    for records_batch in result:
        for i in records_batch:
            print(i,"\n")
        answer = input("Press Enter to continue. Press Q to exit.\n>>> ")
        if answer.upper() == "Q":
            break
    return f"{TerminalColors.OKGREEN}{TerminalColors.UNDERLINE}Total contacts: {len(contacts)}.{TerminalColors.ENDC}"


@input_error
def add(items, name):
    for item in items:
        if item == "contact":
            if name not in contacts:
                phone = input("Enter the phone: ")
                record = Record(name, phone)
                contacts.add_record(record)
            else:
                return "Contact already exists."
        else:
            record:Record = contacts[name]
            if item == "phone":
                phone = input("Enter the phone: ")
                record.add_phone(phone)
            elif item == "email":
                email = input("Enter the email: ")
                record.add_email(email)
            elif item == "birthday":
                birthday = input("Enter the birthday: ")
                record.add_birthday(birthday)
            elif item == "address":
                address = input("Enter the address: ")
                record.add_address(address)
            else:
                return f"{TerminalColors.FAIL}Error: Invalid item.{TerminalColors.ENDC}"
    return f"{TerminalColors.OKGREEN}{TerminalColors.UNDERLINE}Success! {', '.join(items)} have been added.{TerminalColors.ENDC}"

@input_error
def edit(items, name):
    if name not in contacts:
        return "Contact doesn't exist."

    record = contacts[name]
    for item in items:
        if item == "phone":
            phone_to_edit = input("Enter the phone you want to change: ")
            new_phone = input("Enter the new phone number: ")
            record.edit_phone(phone_to_edit, new_phone)
        
        elif item in record:
            new_value = input(f"Enter the new {item}: ")
            record[item] = new_value
        
        else:
            return f"{TerminalColors.FAIL}Error: Invalid item.{TerminalColors.ENDC}"
    return f"{TerminalColors.OKGREEN}{TerminalColors.UNDERLINE}Success! {', '.join(items)} have been edited for {name}.{TerminalColors.ENDC}"


command_maps = {
    "hello" : hello,
    "bye" : bye,
    "add": add,
    "showall": showall,
    "edit": edit,
}
items_list = {
    "contact": True,
    "phone": True, 
    "email": True, 
    "birthday": True, 
    "address": True, 
    "note": True,
}

def main():
    print("Welcome to Virtual Assistant!")

    while True:
        print(f"\n{TerminalColors.HEADER}Available commands: hello, add, change, delete, showall.{TerminalColors.ENDC}")
        user_input = input("Enter the command: ").lower()
        if not user_input:
            print("Provide a command.")
            continue
        command = user_input.split()[0]

        if command not in command_maps:
            print("Provide valid command.")
            continue

        if command in ["hello", "showall"]:
            print(command_maps[command]())
            continue
        elif command in ["bye", "good bye", "exit", "close"]:
            print(command_maps["bye"]())
            break
        else:
            items = input(f"What would you like to {command}?: ").split(', ')

            name = input("Enter the name: ")
            
            print(command_maps[command](items, name))



if __name__ == "__main__":
    main()
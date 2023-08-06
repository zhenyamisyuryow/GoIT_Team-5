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
                try:
                    record = Record(name, phone)
                except Exception as e:
                    return f"{TerminalColors.FAIL}{TerminalColors.UNDERLINE}{e}{TerminalColors.ENDC}"
                contacts.add_record(record)
            else:
                return "Contact already exists."
        else:
            try:
                record:Record = contacts[name]
            except KeyError:
                return f"{TerminalColors.FAIL}{TerminalColors.UNDERLINE}Error: contact {name} doesn't exist.{TerminalColors.ENDC}"
            item_maps = {
                "phone": record.add_phone,
                "email": record.add_email,
                "birthday": record.add_birthday,
                "address": record.add_address,
            }
            item_input = input(f"Enter the {item}: ")
            try:
                item_maps[item](item_input)
            except Exception as e:
                return f"{TerminalColors.FAIL}{TerminalColors.UNDERLINE}{e}{TerminalColors.ENDC}"
    return f"{TerminalColors.OKGREEN}{TerminalColors.UNDERLINE}Success! {', '.join(items)} have been added.{TerminalColors.ENDC}"

def congratulate():
    while True:
        try:
            return contacts.congratulate_period(int(input(f"Enter the number of days for congratulations:> ")))
        except:
            pass
    

command_maps = {
    "hello" : hello,
    "bye" : bye,
    "add" : add,
    "showall" : showall,
    "congratulate" : congratulate
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

    contacts.load_book()
    

    while True:
        print(f"\n{TerminalColors.HEADER}Available commands: hello, add, change, delete, showall, congratulate, bye.{TerminalColors.ENDC}")
        user_input = input("Enter the command: ").lower()
        if not user_input:
            print(f"{TerminalColors.FAIL}{TerminalColors.UNDERLINE}Error: Provide a command.{TerminalColors.ENDC}")
            continue
        command = user_input.split()[0]

        if command not in command_maps:
            print(f"{TerminalColors.FAIL}{TerminalColors.UNDERLINE}Error: Provide valid command.{TerminalColors.ENDC}")
            continue

        if command in ["hello", "showall", "congratulate"]:
            print(command_maps[command]())
            continue
        elif command in ["bye", "good bye", "exit", "close"]:
            print(command_maps["bye"]())
            contacts.save_book()
            break
        else:
            items = input(f"What would you like to {command}?: ").split(', ')
            try:
                [items_list[item] for item in items]
            except KeyError as e:
                print(f"{TerminalColors.FAIL}{TerminalColors.UNDERLINE}Error: can not {command} {e}.{TerminalColors.ENDC}")
                print(f"{TerminalColors.HEADER}Available options are: {', '.join(items_list.keys())}.{TerminalColors.ENDC}")
                continue
            name = input("Enter the name: ")
            
            print(command_maps[command](items, name))



if __name__ == "__main__":
    main()
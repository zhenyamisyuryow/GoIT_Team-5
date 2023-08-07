from base_cls import *


contacts = Contacts()
notes = Notes()

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
def add(items, name):
    for item in items:
        if item == "contact":
            if name not in contacts:
                phone = input("Enter the phone: ")
                try:
                    record = Record(name, phone)
                except Exception as e:
                    return f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}"
                contacts.add_record(record)
            else:
                return "Contact already exists."
        elif item == "note":
            content = input("Enter the content: ")
            tags = input("Add tags: ")
            if tags:
                tags.split(', ')
            notes.add_note(Note(name, content, tags))
        else:
            try:
                record:Record = contacts[name]
            except KeyError:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: contact {name} doesn't exist.{Colors.ENDC}"
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
                return f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}"
    return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {', '.join(items)} have been added.{Colors.ENDC}"




@input_error
def congratulate():
    while True:
        try:
            return contacts.congratulate_period(int(input(f"Enter the number of days for congratulations:> ")))
        except:
            pass

@input_error   
def search():
    while True:
        choice = input(f"What would you like to search : {Colors.HEADER}contact{Colors.ENDC} or {Colors.HEADER}note{Colors.ENDC}: ")
        if choice.lower() == "contact":
            return contacts.search_contacts(input(f"Enter the query for search: "))
        elif choice.lower() == "note":
            result = notes.search_note(input("Enter the query for search: "))
            if len(result) > 0:
                print("\nSearch results:\n")
                for i in result:
                    print(str(i) + "\n")
                break            
            else:
                print(f"No notes were found")        
        
    # return contacts.congratulate_period(int(input(f"Enter the number of days for congratulations:> ")))
    
@input_error
def showall():
    item = input("Available options: contacts, notes\nWhat would you like to see?: ")
    if not item or item not in ["contacts", "notes"]:
        return f"{Colors.FAIL}{Colors.UNDERLINE}Option not available {len(contacts)}.{Colors.ENDC}"
    elif item == "notes":
        choice = input("Do you wish sort notes by tags? y/n: ")
        if choice.lower() == "y":
            result = [str(x) for x in notes.sort_by_tag()]
            return '\n\n'.join(result)
        elif choice.lower() == "n":    
            result = [str(x) for x in notes.values()]
            return '\n\n'.join(result)
    else:
        try:
            number = int(input("How many records would you like to retrieve in one iteration?\n>>> "))
        except ValueError:
            return f"{Colors.FAIL}{Colors.UNDERLINE}Provide number.{Colors.ENDC}"
        result = contacts.iterator(number)
        for records_batch in result:
            for i in records_batch:
                print(i,"\n")
            answer = input("Press Enter to continue. Press Q to exit.\n>>> ")
            if answer.upper() == "Q":
                break
        return f"{Colors.OKGREEN}{Colors.UNDERLINE}Total contacts: {len(contacts)}.{Colors.ENDC}"

       
command_maps = {
    "hello" : hello,
    "bye" : bye,
    "add" : add,
    "search" : search,
    "showall" : showall,
    "congratulate" : congratulate,
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
        print(f"\n{Colors.HEADER}Available commands: hello, add, change, delete, showall, congratulate, search, bye.{Colors.ENDC}")
        user_input = input("Enter the command: ").lower()
        if not user_input:
            print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide a command.{Colors.ENDC}")
            continue
        command = user_input.split()[0]

        if command not in command_maps:
            print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide valid command.{Colors.ENDC}")
            continue

        if command in ["hello", "showall", "congratulate", "search"]:
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
                print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: can not {command} {e}.{Colors.ENDC}")
                print(f"{Colors.HEADER}Available options are: {', '.join(items_list.keys())}.{Colors.ENDC}")
                continue
            name = input("Enter the name (or title): ")
            
            print(command_maps[command](items, name))



if __name__ == "__main__":
    main()
from base_cls import *


contacts = Contacts()
notes = Notes()
filename = "data.bin"

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
            content = input("Enter the content: ").lower()
            try:
                tags = input("Add tags: ").lower().split(", ")
                notes.add_note(Note(name, content, tags))
            except:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide tags{Colors.ENDC}"
        elif item == "tags":
            try:
                tags = input("Add tags: ").lower().split(", ")
                notes[name].add_tags(tags)
            except:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide tags{Colors.ENDC}"
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
            item_input = input(f"Enter the {item}: ").lower()
            try:
                item_maps[item](item_input)
            except Exception as e:
                return f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}"
    return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {', '.join(items)} have been added.{Colors.ENDC}"


@input_error
def edit(items, name):
    try:
        record: Record = contacts[name]
    except KeyError:
        return f"{Colors.FAIL}{Colors.UNDERLINE}Error: contact {name} doesn't exist.{Colors.ENDC}"

    item_maps = {
        "phone": record.add_phone,
        "email": record.add_email,
        "birthday": record.add_birthday,
        "address": record.add_address,
    }

    for item in items:
        if item == "phone":
            if len(record.phones) == 1:
                new_phone = input("Enter the new phone number: ")
                try:
                    record.phones[0] = new_phone
                except Exception as e:
                    return f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}"
            elif len(record.phones) > 1:
                print("Select a phone number to edit:")
                for idx, phone in enumerate(record.phones):
                    print(f"{idx + 1}. {phone}")
                choice = input("Enter the number of the phone to edit: ")
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(record.phones):
                        new_phone = input("Enter the new phone number: ")
                        record.phones[choice_idx] = new_phone

                    else:
                        return "Error: Invalid choice."
                except ValueError:
                    return "Error: Invalid choice."
            else:
                return "Error: No phone numbers available to edit."
        elif item in item_maps:
            new_value = input(f"Enter the new {item}: ")
            try:
                item_maps[item](new_value)

            except Exception as e:
                return f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}"
        else:
            return f"{Colors.FAIL}{Colors.UNDERLINE}Error: {item} cannot be edited.{Colors.ENDC}"
    return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {', '.join(items)} have been edited.{Colors.ENDC}"

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
        choice = input(f"What would you like to search : {Colors.HEADER}contact{Colors.ENDC} or {Colors.HEADER}note{Colors.ENDC}: ").lower()
        if choice == "contact":
            return contacts.search_contacts(input(f"Enter the query for search: "))
        elif choice == "note":
            return notes.search_note(input(f"Enter the query for search: "))
        
@input_error       
def delete_phone(name):
    for i in range(len(contacts[name].phones)):
                print(f"{i + 1}. {contacts[name].phones[i]}")
    choice = int(input("Select the phone number to edit (enter the number): ")) - 1
    return contacts[name].delete_phone(choice)
    
    
def delete_contact(name):
    return contacts.delete_record(name)
    

def delete_note(name):
    return notes.delete_note(name)
    
    

@input_error       
def delete():
    delete_options = {
        "phone" : delete_phone,
        "contact" : delete_contact,
        "note" : delete_note
    }
    
    command = input(f"What would you like to delete: {Colors.HEADER}{', '.join(delete_options)}{Colors.ENDC} ").lower()
    return delete_options[command](input(f"Enter the name of {command}: ")).lower()

    
@input_error
def showall():
    item = input(f"{Colors.HEADER}Available options: contacts, notes{Colors.ENDC}\nWhat would you like to see?: ").lower()
    if not item or item not in ["contacts", "notes"]:
        return f"{Colors.FAIL}{Colors.UNDERLINE}Option not available {len(contacts)}.{Colors.ENDC}"
    elif item == "notes":
        result = [str(x) for x in notes.values()]
        print("\n")
        return '\n'.join(result)
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

def load_books(filename):
    try:
        with open(filename, "rb") as fh:
            contacts.load_book(fh)
            notes.load_book(fh)
    except FileNotFoundError:
        pass
    
def save_book(filename):
    with open(filename, "wb") as fh:
        contacts.save_book(fh)
        notes.save_book(fh)   
      
command_maps = {
    "hello" : hello,
    "bye" : bye,
    "add" : add,
    "search" : search,
    "showall" : showall,
    "congratulate" : congratulate,
    "edit" : edit,
    "delete" : delete
}
items_list = {
    "contact": True,
    "phone": True, 
    "email": True, 
    "birthday": True, 
    "address": True, 
    "note": True,
    "tags": True,
}

    
def main():
    print("Welcome to Virtual Assistant!")
    
    load_books(filename)

    while True:
        print(f"\n{Colors.HEADER}Available commands: hello, add, edit, delete, showall, congratulate, search, bye.{Colors.ENDC}")
        user_input = input("Enter the command: ").lower()
        if not user_input:
            print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide a command.{Colors.ENDC}")
            continue
        command = user_input.split()[0]

        if command in ["hello", "showall", "congratulate", "search", "delete"]:
            print(command_maps[command]())
            continue
        elif command in ["bye", "good bye", "exit", "close"]:
            print(command_maps["bye"]())
            save_book(filename)
            break
        elif command not in command_maps:
            print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide valid command.{Colors.ENDC}")
            continue
        else:
            items = input(f"What would you like to {command}?: ").lower().split(', ')
            try:
                [items_list[item] for item in items]
            except KeyError as e:
                print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: can not {command} {e}.{Colors.ENDC}")
                print(f"{Colors.HEADER}Available options are: {', '.join(items_list.keys())}.{Colors.ENDC}")
                continue
            name = input("Enter the name (or title): ").lower()
            print(command_maps[command](items, name))



if __name__ == "__main__":
    main()
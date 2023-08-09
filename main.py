from base_cls import *
import os
import sort


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
    save_book(filename)
    return "Good bye!"


def help():
    help_text = """
    Available commands:
    hello - type "hello" to display a greeting message
    add - type "add" to add new item
    edit - type "edit" to edit existing item
    bye - type "bye" to save and exit the program
    delete - type "delete" to delete items from contacts or notes
    search - type "search" to search for contacts or notes
    showall - type "showall" to display all contacts or notes
    congratulate - type "congratulate" to display contacts with birthday in the entered period
    clean folder - type "clean folder" to organize files in a folder

    Available items:
    phone - required format is: +380(XX)XXX-XX-XX
    birthday - required format is: MM-DD-YYYY
    """
    return help_text


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

    for item in items:
        if item == "note":
            try:
                title = input("Enter new title (Press Enter to skip): ").lower()
                content = input("Enter new content (Press Enter to skip): ").lower()
                tags = input("Enter new tags (Press Enter to skip): ").lower()
                notes.edit_note(name, title = title, content=content, tags=tags)
            except:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: note with such name doesn't exist.{Colors.ENDC}"
        else:
            try:
                record: Record = contacts[name]
            except:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: contact {name} doesn't exist.{Colors.ENDC}"

            item_maps = {
                "phone": record.edit_phone,
                "email": record.edit_email,
                "birthday": record.edit_birthday,
                "address": record.edit_address,
            }
            if item == "phone":
                if len(record.phones) == 1:
                    new_phone = input("Enter the new phone number: ")
                    try:
                        record.phones[0] = Phone(new_phone)
                    except Exception as e:
                        return f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}"
                elif len(record.phones) > 1:
                    print("Available phones:")
                    for idx, phone in enumerate(record.phones):
                        print(f"{idx + 1}. {phone}")
                    try:
                        choice = int(input("Enter the number of the phone to edit: "))-1
                        if 0 <= choice < len(record.phones):
                            new_phone = input("Enter the new phone number: ")
                            try:
                                record.phones[choice] = Phone(new_phone)
                            except ValueError as e:
                                return e
                        else:
                            return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Invalid choice.{Colors.ENDC}"
                    except ValueError:
                        return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Invalid choice.{Colors.ENDC}"
                else:
                    return f"{Colors.FAIL}{Colors.UNDERLINE}Error: No phone numbers available.{Colors.ENDC}"
            elif item in item_maps:
                new_value = input(f"Enter the new {item}: ").lower()
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
        choice = input(f"What would you like to search {Colors.HEADER}contact{Colors.ENDC} or {Colors.HEADER}note{Colors.ENDC}?: ").lower()
        if choice == "contact":
            try:
                return '\n' + contacts.search_contacts(input(f"Enter the query for search: ").lower())
            except:
                print(f"{Colors.WARNING}{Colors.UNDERLINE}Provide query for the search!{Colors.ENDC}")
                continue
        elif choice == "note":
            return notes.search_note(input("Enter the query for search: ").lower())
        else:
            return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Choose between available options: contact, note{Colors.ENDC}"     
    
    
@input_error       
def delete(items, name):
    for item in items:
        if item == "note":
            try:
                notes.pop(name)
            except:
                return f"{Colors.WARNING}{Colors.UNDERLINE}Note was not found.{Colors.ENDC}"
        elif item == "contact":
            try:
                contacts.pop(name)
            except:
                return f"{Colors.WARNING}{Colors.UNDERLINE}Contact was not found.{Colors.ENDC}"
        else:
            record:Record = contacts[name]
            for key, item in zip(vars(record), items):
                if item == key:
                    vars(record)[key] = None
                elif item == "phone":
                    if len(record.phones) <= 1:
                        record.phones = None
                    else:
                        print("Available phones: ")
                        for idx, phone in enumerate(record.phones):
                            print(f"{idx + 1}. {phone}")
                        try:
                            choice = int(input("Enter the number of the phone to delete: ")) -1
                            del record.phones[choice]
                        except ValueError:
                            return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Invalid choice.{Colors.ENDC}"
    return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {item} has been deleted!{Colors.ENDC}"

    
@input_error
def showall():
    item = input(f"{Colors.HEADER}Available options: contacts, notes{Colors.ENDC}\nWhat would you like to see?: ").lower()
    if not item or item not in ["contacts", "notes"]:
        return f"{Colors.FAIL}{Colors.UNDERLINE}Option not available {item}.{Colors.ENDC}"
    elif item == "notes":
        if not notes:
            return f"{Colors.WARNING}{Colors.UNDERLINE}No notes were found.{Colors.ENDC}"
        choice = input("Do you wish to sort notes by tags? y/n: ")
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

def clean():
    pass
      
command_maps = {
    "hello" : hello,
    "bye" : bye,
    "help": help,
    "add" : add,
    "edit" : edit,
    "delete" : delete,
    "search" : search,
    "showall" : showall,
    "congratulate" : congratulate,
    "clean folder": sort.organize_files
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
        print(f"\n{Colors.HEADER}Available commands: {', '.join(command_maps.keys())}.{Colors.ENDC}")
        user_input = input("Enter the command: ").lower()
        if not user_input:
            print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide a command.{Colors.ENDC}")
            continue
        command = user_input.split()[0]

        if command in ["hello", "help", "showall", "congratulate", "search"]:
            print(command_maps[command]())
            continue
        elif command in ["bye", "good bye", "exit", "close"]:
            print(command_maps["bye"]())
            break
        elif user_input == "clean folder":
            folder = input("Enter the path of the folder to organize: ")
            command_maps["clean folder"](folder)
            continue
        elif command not in command_maps:
            print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide valid command.{Colors.ENDC}")
            continue
        else:
            items = input(f"What would you like to {command}?: ").lower().split(', ')
            for item in items:
                if item == "note":
                    name = input("Enter note title: ").lower()
                    print(command_maps[command]([item], name))
                    items.remove(item)
            if len(items) < 1:
                continue
            name = input("Enter the name of the contact: ").lower()
            print(command_maps[command](items, name))



if __name__ == "__main__":
    main()
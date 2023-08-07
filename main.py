from base_cls import *
import pickle


filename = "data.bin"
contacts = Contacts()
notes = Notes()



def load_books():
    global contacts, notes
    
    try:
        with open (filename, "rb") as fh:

            try:
                contacts = pickle.load(fh)
            except EOFError:
                pass
            
            try:   
                notes = pickle.load(fh)
            except EOFError:
                pass
        return contacts, notes
    except FileNotFoundError:
        return contacts, notes

    
def save_books(contacts, notes):
    with open (filename, "wb") as fh:
        pickle.dump(contacts, fh)
        pickle.dump(notes, fh)






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
    try:
        number = int(input("How many records would you like to retrieve in one iteration?\n>>> "))
    except ValueError:
        return f"{TerminalColors.FAIL}{TerminalColors.UNDERLINE}Provide number.{TerminalColors.ENDC}"
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
                    return f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}"
                contacts.add_record(record)
            else:
                return "Contact already exists."
        elif item == "note":
            content = input("Enter the content: ")
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
            item_input = input(f"Enter the {item}: ")
            try:
                item_maps[item](item_input)
            except Exception as e:
                return f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}"
    return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {', '.join(items)} have been added.{Colors.ENDC}"




# @input_error
def edit(items, name):
    if name not in contacts:
        return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Contact doesn't exist.{Colors.ENDC}"

    record = contacts[name]
    phone_list = record.phones
    if "phone" in items and len(phone_list)>1:
        try:
            for i in range(len(phone_list)):
                print(f"{i + 1}. {phone_list[i]}")
            choice = int(input("Select the phone number to edit (enter the number): ")) - 1
        except:
            return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide a digit.{Colors.ENDC}"
        if 0 <= choice < len(phone_list):
            new_phone = input("Enter the new phone number: ")
            record.edit_phone(phone_list[choice], new_phone)
            return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! Phone number edited for {name}.{Colors.ENDC}"
        else:
            return "Invalid choice."
    for item in items:
        if item in record:
            new_value = input(f"Enter the new {item}: ")
            record[item] = new_value
        
        else:
            return f"{Colors.FAIL}Error: Invalid item.{Colors.ENDC}"
    return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {', '.join(items)} have been edited for {name}.{Colors.ENDC}"

@input_error
def congratulate():
    while True:
        try:
            return contacts.congratulate_period(int(input(f"Enter the number of days for congratulations:> ")))
        except:
            pass



@input_error       
def delete_phone(name):
        
    return contacts[name].delete_phone(Phone(input(f"Enter the phone: ")))
    
    
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
    
    
    command = input(f"What would you like to delete: {TerminalColors.HEADER}{', '.join(delete_options)}{TerminalColors.ENDC} ")
    return delete_options[command](input(f"Enter the name of {command}: "))
    
        
        

@input_error   

def search():
    while True:
        choice = input(f"What would you like to search : {Colors.HEADER}contact{Colors.ENDC} or {Colors.HEADER}note{Colors.ENDC}: ")
        if choice.lower() == "contact":
            return contacts.search_contacts(input(f"Enter the query for search: "))
        elif choice.lower() == "note":
            break
        
    
    
@input_error
def showall():
    item = input(f"{Colors.HEADER}Available options: contacts, notes{Colors.ENDC}\nWhat would you like to see?: ")
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

       
          
command_maps = {
    "hello" : hello,
    "bye" : bye,
    "add" : add,
    "search" : search,
    "showall" : showall,
    "congratulate" : congratulate,

    "search" : search,
    "delete" : delete
    "edit" : edit,

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

    contacts, notes = load_books()[0], load_books()[1]
    

    while True:
        print(f"\n{Colors.HEADER}Available commands: hello, add, change, delete, showall, congratulate, search, bye.{Colors.ENDC}")
        user_input = input("Enter the command: ").lower()
        if not user_input:
            print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide a command.{Colors.ENDC}")
            continue
        command = user_input.split()[0]


        if command not in command_maps:
            print(f"{TerminalColors.FAIL}{TerminalColors.UNDERLINE}Error: Provide valid command.{TerminalColors.ENDC}")
            continue

        if command in ["hello", "showall", "congratulate", "search", "delete"]:


            print(command_maps[command]())
            continue
        elif command in ["bye", "good bye", "exit", "close"]:
            print(command_maps["bye"]())
            save_books(contacts, notes)
            break
        elif command not in command_maps:
            print(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide valid command.{Colors.ENDC}")
            continue
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
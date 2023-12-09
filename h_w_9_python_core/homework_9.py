def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "There is no such user in your contacts list"
        except ValueError:
            return "Enter name and phone"
        except IndexError:
            "It`s not valid command"
    return wrapper

contacts = {}

@input_error
def hello():
    return "How can I help you?"

@input_error
def add_contact(name, phone):
    contacts[name] = phone
    return f"You add {name} with this phone number: {phone}"

@input_error
def change_phone(name, phone):
    if name in contacts:
        contacts[name] = phone
        return f"The contact {name} has changed phone number on {phone}"
    else:
        raise KeyError

@input_error
def show_phone(name):
    if name in contacts:
        return f"Contact {name} has phone number : {contacts[name]}"
    else:
        raise KeyError
    
@input_error
def show_all():
    if not contacts:
        return "There is no contacts"
    else:
        result = "Your contacts:\n"
        for name, phone in contacts.items():
            result += f"{name}: {phone}\n"
        return result.strip()
    
@input_error
def close_program():
    return "Good bye."

def handler(command):
    if command.lower() == "hello":
        return hello()
    
    elif command.lower().startswith("add "):
        _, name, phone = command.split()
        return add_contact(name, phone)
    
    elif command.lower().startswith("change "):
        _, name, phone = command.split()
        return change_phone(name, phone)
    
    elif command.lower().startswith("phone "):
        _, name = command.split()
        return show_phone(name)
    
    elif command.lower() == "show all":
        return show_all()
    
    elif command.lower() in ["good bye", "close", "exit"]:
        return close_program()
    
    else:
        raise ValueError
    
def main():
    while True:
        user_input = input("Please, enter command: ")
        if user_input.lower() in ["good bye", "close", "exit"]:
            print(handler(user_input))
            break
        else:
            try:
                result = handler(user_input)
                print(result)
            except ValueError as Error:
                print(Error)
                
if __name__ == "__main__":
    main()

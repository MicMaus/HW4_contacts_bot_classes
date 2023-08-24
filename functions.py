from error_handl_decorator import error_handling_decorator
from error_handl_decorator import CustomError
from collections import UserDict
import re

#classes
class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self):
        return self.value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(str(value)) 

class Record:
    def __init__(self, name, phone=None): #mandatory and optional atributes
        self.name = Name(value=name)
        self.phones = []
        if phone:
            self.add_new_phone(phone)

    def add_new_phone(self, phone): #add phone number to the list
        self.phones.append(Phone(value=phone))

    def amend_phone(self, name, new_phone, old_phone): #amend phone number
        phone_found = False
        for stored_phone in self.phones.copy():
            if str(stored_phone) == old_phone:
                self.phones.remove(stored_phone)
                self.add_new_phone(new_phone)
                phone_found = True

        if not phone_found:
            raise CustomError("phone number was not found")
        # self.phones.clear()
        # self.add_new_phone(phone)

    def remove_phone(self, phone):
        phone_found = False
        for stored_phone in self.phones.copy():
            if str(stored_phone) == phone:
                self.phones.remove(stored_phone)
                phone_found = True

        if not phone_found:
            raise CustomError("phone number was not found")

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

phone_book  = AddressBook()

#parser
@error_handling_decorator
def parse_input(user_input):
    for request in commands.keys():
        if user_input.startswith(request):
            modif_input = user_input.replace(request, '', 1).strip()
            name = modif_input.split(' ')[0]
            matches = re.findall(r'\s(\d+)', modif_input)
            if len(matches) == 1:
                old_number = matches[-1]
                func = commands[request]
                return func(name, old_number)
            elif len(matches) == 2:
                old_number = matches[-1]
                new_number = matches[-2]
                func = commands[request]
                return func(name, new_number, old_number)
            elif len(matches) == 0:
                func = commands[request]
                return func(name)
        
    return "please provide a valid command"

#adding new contact/phone number
def add_contact (name, phone=None): 
    if not name:  #handle situation when name is not provided at all
        raise CustomError("please provide name and phone number divided by space")
    elif name not in phone_book:
        record = Record(name, phone)
        phone_book.add_record(record)
        return("new contact successfully added")
    else:
        record = phone_book[name]
        if not phone.isdigit():
            raise CustomError("please provide name and phone number divided by space")
        record.add_new_phone(phone)
        return("new phone number successfully added to existing contact")
          
#change the phone number
def change_phone (name, new_phone, old_phone):
    if name not in phone_book:
        raise CustomError('name not found')
    if not new_phone or not old_phone:
        raise CustomError("please provide name, new number and old number divided by space")
    
    record = phone_book[name]
    record.amend_phone(name, new_phone, old_phone)
    return("contact successfully changed")
    
#remove the phone number   
def delete_phone(name, phone):
    if name not in phone_book:
        raise CustomError('name not found')
    if not phone:
        raise CustomError("please provide name and phone number divided by space")
    
    record = phone_book[name]
    record.remove_phone(phone)
    return("phone number successfully removed")

#show the phone of user
def show_phone (name): 
    if name not in phone_book:
        raise CustomError("please provide a valid name")
    
    record = phone_book[name]
    phone_numbers = []
        
    for item in record.phones:
        phone_numbers.append(item.value)

    for el in phone_numbers:
        if el.isdigit():
            return f"{name}: {', '.join(phone_numbers)}"
    
    return f"{name}: no phone numbers"

#show all name-phone pairs
def show_all(notused1):
    contacts = []
    for name in phone_book.keys():
        one_contact = show_phone(name)
        contacts.append(one_contact)
    if contacts:
        return ';\n'.join(contacts)
    else:
        raise CustomError("phone book is empty")

def hello(notused1):
    return("How can I help you?")

def search (search_word, phone):
    result= []
    for name, record in phone_book.items():
        phone_numbers = ', '.join(phone.value for phone in record.phones)
        
        if (search_word == name) or (search_word in phone_numbers):
            result.append(f"{name}: {phone_numbers}")

    if result:
        return '; '.join(result)
    else:
        raise CustomError("nothing found")

commands = {
    "add": add_contact,
    "change": change_phone,
    "remove": delete_phone,
    "phone": show_phone,
    "show all": show_all,
    "hello": hello,
    "search": search,
}         

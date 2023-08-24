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
    name = 'UserName'

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

    def amend_phone(self, name, phone): #empty list and add new phone number
        self.phones.clear()
        self.add_new_phone(phone)

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
            phone = ''.join(re.findall(r'\s(\d+)', modif_input))
            func = commands[request]
            return func(request, name, phone)
    return "please provide a valid command"

#adding new contact/phone number
def add_contact (request, name, phone): 
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
def change_phone (request, name, phone):
    if name not in phone_book:
        raise CustomError('name not found')
    if not phone:
        raise CustomError("please provide name and phone number divided by space")
    
    record = phone_book[name]
    record.amend_phone(name, phone)
    return("contact successfully changed")
    
#remove the phone number   
def delete_phone(request, name, phone):
    if name not in phone_book:
        raise CustomError('name not found')
    if not phone:
        raise CustomError("please provide name and phone number divided by space")
    
    record = phone_book[name]
    record.remove_phone(phone)
    return("phone number successfully removed")

#show the phone of user
def show_phone (notused1, name, notused2): 
    if name not in phone_book:
        raise CustomError("please provide a valid name")
    
    record = phone_book[name]
    phone_numbers = []
        
    for item in record.phones:
        phone_numbers.append(item.value)

    for el in phone_numbers:
        if el.isdigit():
            return f"{name}: {', '.join(phone_numbers)}"
    else:
        return f"{name}: no phone numbers"

#show all name-phone pairs
def show_all(notused1, notused2, notused3):
    contacts = []
    for name in phone_book.keys():
        one_contact = show_phone(None, name, None)
        contacts.append(one_contact)
    if contacts:
        return ';\n'.join(contacts)
    else:
        raise CustomError("phone book is empty")

def hello(notused1, notused2, notused3):
    return("How can I help you?")

def search (request, search_word, phone):
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

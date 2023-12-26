from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

    def __str__(self):
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")


class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    @property
    def days_to_birthday(self):
        if not self._value:
            return None
        today = datetime.now()
        birthday = datetime.strptime(self._value, "%Y-%m-%d").replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        return (birthday - today).days


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found in record")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}{birthday_str}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n=5):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i + n]


book = AddressBook()
record1 = Record("Vadim", "2001-09-04")
record1.add_phone("1234567890")
record2 = Record("Vika", "2002-05-14")
record2.add_phone("0987654321")
book.add_record(record1)
book.add_record(record2)

for batch in book.iterator(1):
    for record in batch:
        print(record)
        if record.birthday:
            print(f"Days to birthday: {record.birthday.days_to_birthday}")

import csv

employee_list = []


class Employee:

    def __init__(self, employee_id, name, ssn, phone, email, salary):
        self.employee_id = employee_id
        self.name = name
        self.ssn = str(ssn)
        self.phone = str(phone)
        self.email = email
        self.salary = str(salary)

    def __str__(self):
        return f"{self.employee_id},{self.name},{self.ssn},{self.phone},{self.email},{self.salary}"

    @classmethod
    def get_by_ssn(cls, ssn):
        ssn_list = [employee for employee in employee_list if employee.ssn == ssn]
        return ssn_list

    @staticmethod
    def validate_ssn(input_string):
        while True:
            try: 
                employee_ssn = int(input(input_string))
                assert len(str(employee_ssn)) == 9
                break
            except ValueError:
                print("ssn must be a 9 digit number, with no dashes or spaces.")
            except AssertionError:
                print("ssn must be 9 digits long.")
        return str(employee_ssn)

    @property
    def get_ssn(self):
        return f'{self.ssn[:3]}-{self.ssn[3:5]}-{self.ssn[5:9]}'

    @property
    def get_phone(self):
        return f'({self.phone[:3]}){self.phone[3:6]}-{self.phone[6:10]}'
    

def set_ssn(employee):
    employee_ssn = 'Enter SSN:   '
    employee.ssn = Employee.validate_ssn(employee_ssn)
    print(f'{employee.name} SSN set to {employee.get_ssn}')


def set_phone(employee):
    while True:
        try:
            employeePhone = int(input('Enter phone number:   '))
            assert len(str(employeePhone)) == 10
            break
        except ValueError:
            print("Phone must be a 10 digit number, with no dashes or spaces.   ")
        except AssertionError:
            print("Phone number must be 10 digits long.")
    employee.phone = str(employeePhone)
    print(f"{employee.name}'s phone number set to {employee.get_phone}.")


def set_email(employee):
    employee.email = input('Enter employee email:   ')
    print(f"{employee.name}'s email set to {employee.email}.")


def set_salary(employee):
    employee_salary = input('Enter employees salary:   ')
    employee.salary =  employee_salary.replace('$', '')
    print(f"{employee.name}'s email set to {employee.email}")


def set_name(employee):
    employee.name = input('Enter employees name:   ')
    print(f"{employee.name} name has been set.")


def edit_employee(employee):
    while True:
        try:
            choice = str(input("Enter information to edit.  Choices are name, ssn, phone, email, or salary.\n")).lower()
            if choice == 'name':
                set_name(employee)
            elif choice == 'ssn':
                set_ssn(employee)
            elif choice == 'phone':
                set_phone(employee)
            elif choice == 'email':
                set_email(employee)
            elif choice == 'salary':
                set_salary(employee)
            else:
                print('Invalid selection.')
                break
        except ValueError:
            print('Invalid selection.')
        break


def view_single_employee(employee):
    print(f"""
    ----------------------------{employee.employee_id}. {employee.name} -----------------------------
    SSN: {employee.get_ssn}
    Phone: {employee.get_phone}
    Email: {employee.email}
    Salary: ${employee.salary}
    -----------------------------------------------------------------""")


def edit_selection(employee):
    while True:
        edit_question = input("Would you like to edit this employees information? Type 'yes'.\n")
        if edit_question.lower() == 'yes':
            edit_employee(employee)
        else:
            break


def add_employee():
    new_guy = Employee((len(employee_list)+1), 'name', 'ssn', 'phone', 'email', 'salary')
    set_name(new_guy)
    set_ssn(new_guy)
    set_phone(new_guy)
    set_email(new_guy)
    set_salary(new_guy)

    employee_list.append(new_guy)


def menu():
    print(f'''
    Employee Management System
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    There are {len(employee_list)} employees in the database.

    Type 'add' to add up to 5 employees into the database.
    Type 'all' to view all employees.
    Type 'see' to pull a specific employees information from the database.
    Type 'search' to search employee by SSN.

    To edit an employee, start with 'search' or 'see'.

    Use 'backup' to save any changes to the database.
    Type 'menu' to see this menu again.
    Type 'quit' to quit.
 ''')


def get_selection_for_menu():
    selections = ['add', 'see', 'all', 'quit', 'search', 'menu', 'backup']

    selection = input('Selection:   ')
    selection = selection.lower()

    if selection not in selections:
        print(f'Valid selections are: {", ".join(selections)}')
    else:
        if selection == 'quit':
            write_backup()
            quit()
        elif selection == 'backup':
            write_backup()
        elif selection == 'add':
            add_employee()
            print(f'Add successful.  There are now {len(employee_list)} in the database.')
        elif selection == 'all':
            if len(employee_list) > 0:
                for e in employee_list:
                    view_single_employee(e)
            else:
                print('Employee database is empty.')
        elif selection == 'see':
            while True:
                try:
                    i = int(input(f'Which employee you would like to see by number.'))
                    view_single_employee(employee_list[i-1])
                    try:
                        edit_selection(employee_list[i-1])
                    except:
                        print('Edit Failed.')
                except (IndexError, ValueError):
                    print(f"No employee by that number.  Please enter a number between 1-{len(employee_list)}.")
                break
        elif selection == 'menu':
            menu()
        elif selection == 'search':
            ssn_search = input('Enter ssn with no dashes or spaces:   ')
            employee = Employee.get_by_ssn(ssn_search)
            try:
                view_single_employee(employee[0])
                edit_selection(employee[0])
            except IndexError:
                print('No employees with that SSN in database.')


def write_backup():
    with open('employees.txt', 'w+') as file:
        for employee in employee_list:
            file.write((str(employee)+'\n'))
    print('Employee data saved.')


def read_backup():
    with open('employees.txt', 'r') as file:
        reader = csv.reader(file,  delimiter=',')
        for line in reader:
            employee_id = line[0]
            name = line[1]
            ssn = line[2]
            phone = line[3]
            email = line[4]
            salary = line[5]
            employee = Employee(employee_id, name, ssn, phone, email, salary)
            employee_list.append(employee)
    print('Employee data loaded.')


read_backup()
menu()

while True:
    get_selection_for_menu()
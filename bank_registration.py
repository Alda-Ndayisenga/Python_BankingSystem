class Customer:
    def __init__(self):
        self.Name = ""
        self.Surname = ""
        self.Address = ""
        self.Email = ""

    def _customer_registration(self):
        self.Name = input("Client's name: ")
        self.Surname = input("Client's surname: ")
        self.Address = input("Client's Address: ")
        self.Email = input("Client's email: ")
        while "@" not in self.Email:
            print("Invalid email address")
            self.Email = input("Client's email: ")

    def profile_creation(self):
        self._customer_registration()

    def customer_summary(self):
        print(f"""Here are the customer's details:
         Name = {self.Name}
         Surname = {self.Surname}
         Address = {self.Address}
         Email = {self.Email}
                    """)

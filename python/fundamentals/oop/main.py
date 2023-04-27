# 1
# class Shoe:
#     # now our method has 4 parameters (including self)!
#     def __init__(self, brand, shoe_type, price, in_stock):
#     	# we assign them accordingly
#         self.brand = brand
#         self.type = shoe_type
#         self.price = price
#         # the status is set to True by default
#         self.in_stock = True

# skater_shoe = Shoe("Vans", "Low-top Trainers", 59.99, False)
# dress_shoe = Shoe("Jack & Jill Bootery", "Ballet Flats", 29.99, False)
# print(skater_shoe.type)	# output: Low-top Trainers
# print(dress_shoe.type)	# output: Ballet Flats

# Ninja Challenges!
# Open this code on the Trace website to get a better view of all the variables and their attributes.
# Make a new instance of a shoe
# Update the in_stock attribute to False

# 2
# class Shoe:

#     def __init__(self, brand, shoe_type, price):
#         self.brand = brand
#         self.type = shoe_type
#         self.price = price
#         self.in_stock = True

#     # Takes a float/percent as an argument and reduces the
#     # price of the item by that percentage.
#     def on_sale_by_percent(self, percent_off):
#         self.price = self.price * (1-percent_off)

#     # Returns a total with tax added to the price.
#     def total_with_tax(self, tax_rate):
#         tax = self.price * tax_rate
#         total = self.price + tax
#         return total

#     # Reduces the price by a fixed dollar amount.
#     def cut_price_by(self, amount):
#         if amount < self.price:
#             self.price -= amount
#             return self.price
#         else:
#             print("Price deduction too large.")


# # Create some shoes. Call some methods on those shoes. Print your shoe's attributes..
# my_shoe = Shoe("Converse", "Low-tops", 36.00)
# print(my_shoe.total_with_tax(0.05))
# my_shoe.cut_price_by(10)
# print(my_shoe.price)

# Jason_shoe = Shoe("Nike", "Running", 50.50)
# Kevin_shoe = Shoe("Nike", "Basketball", 73.30)

# print(Jason_shoe.total_with_tax(0.08))
# print(Kevin_shoe.cut_price_by(10))


# # 3
# class Player:
#     def __init__(self, name, age, position, team):
#         self.name = name
#         self.age = age
#         self.position = position
#         self.team = team


# # Uncomment the line below to test
# player_kevin = Player("kevin Durant", 34, "small forward", "Brooklyn Nets")


4.
# Bank Account


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.accounts = [BankAccount(int_rate=0.02, balance=0), BankAccount(
            int_rate=0.02, balance=0)]
        for account_number in range(len(self.accounts)):
            if account_number:
                self.account = self.accounts[account_number - 1]

    def deposit(self, account_number, ammount):
        if account_number:
            self.accounts[account_number-1].balance += ammount
            return self

    def withdrawal(self, account_number, amount):
        if account_number:
            if amount <= self.account.balance:
                self.accounts[account_number-1].balance -= amount
                return self
            else:
                print(
                    f"Please check your account {account_number} balance.")
        return self

    def display_balance(self, account_number):
        if account_number:
            print(
                f"User: {self.name}, account{account_number} Balance: ${self.accounts[account_number - 1].balance}")
            return self

    def transfer_money(self, account_number, other_user, amount):
        if account_number:
            if self.account.balance >= amount:
                self.accounts[account_number - 1].balance -= amount
            else:
                print(f"Please check your account {account_number} balance.")
            other_user.account.balance += amount
        return self

    def self_transfer_money(self, account_number1, account_number2, amount):
        if account_number1:
            if self.account.balance >= amount:
                self.account.balance -= amount
            else:
                print(f"Please check your account {account_number1} balance.")
            self.account_number2 = account_number2
            self.accounts[account_number2 - 1].balance += amount
        return self


class BankAccount:
    def __init__(self, int_rate=0.02, balance=0):
        self.int_rate = int_rate
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Please check your balance first.")

    def display_account_info(self):
        print(f"Balance: ${self.balance}")

    def yield_interest(self, int_rate=0.05):
        if self.balance > 0:
            self.balance += self.balance * self.int_rate
            return self


Jason = User("Jason", "jason@gmail.com")
Kevin = User("Kevin", "kevin@gmail.com")
Jack = User("Jack", "jack@gmail.com")

Jason.deposit(1, 500).withdrawal(1, 100).self_transfer_money(
    1, 2, 200).display_balance(1)
Jason.deposit(2, 300).withdrawal(
    2, 100).transfer_money(2, Kevin, 50).display_balance(2)
Kevin.display_balance(1)


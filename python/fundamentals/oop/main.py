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


# 3
class Player:
    def __init__(self, name, age, position, team):
        self.name = name
        self.age = age
        self.position = position
        self.team = team

    def print_Player(self):
        print(f'{self.name} = {"name": {self.name}, "age": {self.age}, "position": {self.position}, "team": {self.team}}')


# Uncomment the line below to test
player_kevin = Player("kevin Durant", 34, "small forward", "Brooklyn Nets")
print(player_kevin.name)
print(player_kevin.print_Player())

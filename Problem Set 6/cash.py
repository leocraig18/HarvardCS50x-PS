# TODO
from cs50 import get_float

# Create function for get cents.


def get_cents():
    while True:
        cents = (get_float("Change owed: ")) * 100
        if cents > 0:
            break
    return cents

# Create function for quarters owed.


def calculate_quarters(cents):

    quarters = 0
    while cents >= 25:
        cents = cents - 25
        quarters = quarters + 1
        if cents < 25:
            break
    return quarters

# Calculate function for dimes owed.


def calculate_dimes(cents):
    dimes = 0
    while cents >= 10:
        cents = cents - 10
        dimes = dimes + 1
        if cents < 10:
            break
    return dimes

# Calculate function for nickels owed


def calculate_nickels(cents):
    nickels = 0
    while cents >= 5:
        cents = cents - 5
        nickels = nickels + 1
        if cents < 5:
            break
    return nickels

# Calculate function for pennies owed


def calculate_pennies(cents):
    pennies = 0
    while cents >= 1:
        cents = cents - 1
        pennies = pennies + 1
        if cents == 0:
            break
    return pennies


# Ask how many cents the customer is owed
cents = (int(get_cents()))

# Number of quarters to give to customer
quarters = calculate_quarters(cents)
cents = cents - (quarters * 25)

# Number of dimes
dimes = calculate_dimes(cents)
cents = cents - (dimes * 10)

# Number of nickels
nickels = calculate_nickels(cents)
cents = cents - (nickels * 5)

# Number of pennies
pennies = calculate_pennies(cents)
cents = cents - (pennies)

# Sum coins
coins = (quarters + dimes + nickels + pennies)

# Print total
print(f"{coins} coins")
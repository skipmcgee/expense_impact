#!/usr/bin/env python3
#
#######################################################################################################
#
#
# TLDR: Run this script in the superior OS (Linux, obvi) or the inferior OS (Windows, ugh) when
# contemplating an annutitized expense (Netflix, Amazon Prime, Cable TV, other recurring service).
#
# Written by Skip McGee, 20200824, for DJC2 20.2 AKA "The Looters"
# The primary purpose of the script is to get folks thinking about the total cost of personal expenses.
# Annuitized expenses often appear supportable when their total cost is actually absurd.
# For example, look at the total cost of a daily $3.50 coffee - that addiction requires a lot of $!
# The secondary purpose is to get some repetitions messing around in python & running a script.
# There are several embedded "goodies" in the script - opportunities for improvement.
#
# Directions for running this script in Windows:
# -Browse to https://www.python.org/downloads/
# -Download the current version of python and Run (no admin / elevated privilege should be required).
# -Save this script and right-click "Edit with IDLE". Now you are ready to make changes to the script!
# -Click Run => Run Module or use the F5 command to run the expense_impact.py
#
#
#######################################################################################################


# import statements for requred python modules would go here if needed
# import numpy
# import math


error_number = 0 # Need to establish this variable value initially so that we can change it later

# Define user input as variables for future use within the script
# Using different functions here allows for independent calls or granular error checking
def expense_input():
  try:
    global expense 
    expense = round(float(input("Enter an expense amount in dollars (example - 1.50): $")),2)
  except ValueError:
    print("Error while defining expense, please try again.")
    error_counter() # Call our error counting function - more on that later.
    expense_input() # Recursively call the input so the user can re-enter the correct value.


def interval_input():
  try:
    global interval
    interval = int(input("Enter the expense recurrence time interval, Daily = 1, Weekly = 2, Monthly = 3, Yearly = 4: "))
  except ValueError:
    error_counter()
    print("Error while defining time interval, please try again.")
    interval_input()


def age_input():
  try: # what is this 'try' syntax? Why use it?
    global age
    age = int(input("Enter your current age in years (example - 23): "))
  except ValueError:
    error_counter()
    print("Error while defining age, please try again.")
    age_input()


def interest_input():
  try:
    global interest_rate
    interest_rate = round(float(input("Enter your projected/anticipated after-tax real interest rate until age 60 (example - 5 or 6 percent: ")),2)
    interest_rate = round((interest_rate / 100),2)
  except ValueError:
    error_counter()
    print("Error while defining interest rate, please try again.")
    interest_input()


def inflation_input():
  try:
    global inflation
    inflation = round(float(input("Enter your best guess at your projected inflation rate until age 60 (example - 2 or 3 percent): ")),2)
    inflation = round((inflation / 100),2)
  except ValueError:
    error_counter()
    print("Error while defining inflation rate, please try again.")
    inflation_input()


# Now we want to ensure that the variables that we defined are actually usable input.
# There are a lot of values that wouldn't be useable or make sense, so let's scrub those out.
def input_cleaning():
  try:
    while expense <= 0:
      print("Please enter a number.")
      expense_input()
    while interval <= 0:
      print("Please enter an integer.")
      interval_input()
    while interval >= 5:
      print("Please enter an integer.")
      interval_input()
    while age <= 0:
      print("Please enter an age greater than 0")
      age_input()
    while age >= 120:
      print("Please enter an age less than 120, you probably are mentally", age)
      age_input()
    while interest_rate <= 0:
      print("Please enter an interest rate greater than 0")
      interest_input()
    while interest_rate >= 99:
      print("Please enter an interest rate less than 199%")
      interest_input()
    while inflation <= 0:
      print("Please enter an inflation rate greater than 0")
      inflation_input()
    while inflation >= 5:
      print("Please enter an inflation rate less than 500%")
      inflation_input()
# Notice the generic catch-all "except" statements doesn't identify the specific expected error
  except:
    error_counter()
    errors(1) # Note the first call of the errors function with a parameter.


def calcs():
# Why do we need global variables here? Check out this description of python scopes if you would like a quick review:
# https://www.w3schools.com/python/python_scope.asp
# Here are the actual calculations the script is running.
# Note that one assumption is a Safe Withdrawal Rate of 4% yearly (equal to 25 x the yearly expense). This SWR is based on the Trinity Study which
# can be found at https://www.bogleheads.org/wiki/Safe_withdrawal_rates.
# Another assumption is that retirement age is 62... (See GOODIE #3)
  global current_value
  global future_value
  global interval_string
  global monthly_savings
  interval_string = ""
  compounding_years = (62-age)
  try:
    if interval == 1:
      interval_string = "daily"
      current_value = (365.25 * expense) * 25
      current_value = round(current_value,2)
      future_value = round(current_value * ((1 + inflation) ** compounding_years),2)
    elif interval == 2: # why would you use an 'elif' instead of an 'if' statement?
      interval_string = "weekly"
      current_value = ((expense / 7) * 365.25) * 25
      future_value = round(current_value * (1 + inflation ** compounding_years),2)
    elif interval == 3:
      interval_string = "monthly"
      current_value = (expense * 12) * 25
      future_value = round(current_value * ((1 + inflation) ** compounding_years),2)
    elif interval == 4:
      interval_string = "yearly"
      current_value = expense * 25 
      future_value = round(current_value * ((1 + inflation) ** compounding_years),2)
    nominal_inflation = (interest_rate + inflation + (interest_rate * inflation))
    monthly_savings = round(((((interest_rate/12) * future_value) / (1 + (interest_rate/12)**compounding_years) - 1)),2)
    
  except:
    error_counter()
    errors(2)
    

# We keep the script results in a separate function to enable troubleshooting. Do we need an error checker here?
def output():
  # Note the f-string syntax that entered with python3.6ish and how easy it is to print a variable value.
  first_line = f"The amount of money that you would need to fund a {interval_string} ${expense} expense from {age} years old until death is ${current_value}"
  second_line = f"The amount of money that you would need to fund a {interval_string} ${expense} expense (in current dollars) from 62 years old until death is ${future_value} (in future dollars)."
  third_line = f"You would need to save ${monthly_savings} monthly until age 62 to be able to support your {interval_string} ${expense} expense (in current dollars) in retirement."
  print("*****")
  print("Script Output:")
  print(first_line)
  print(second_line)
  print("*****") # these print shenanigans just make the output look a bit cooler since the script is so simple.
  print(third_line)
  print("*****")


# Now for the errors functions - we want to know if we had any issues, and if there was a problem, where in the script we should start looking.
# This counter function keeps track of how many errors we had.
def error_counter():
  global error_number
  error_number += 1


# This error function is a crude but effective way of identifying the location of an error.
def errors(error=0):
  if error_number == 0:
    if error == 0:
      print("")
      return print("expense_impact.py ran without errors")
  elif error_number >= 1:
    print("")
    print(error_number, "error(s) occurred while defining the expense_impact.py script variables.")
    if error == 1:
      # GOODIE NUMBER 1: what should these error print statements say? Find where / under what conditions they are called and write print
      # statements to enable future troubleshooting.
      return print("") # first print statement to create
    elif error == 2:
      return print("") # second print statement to create
    elif error >= 3:
      return # These options are not needed at this time


# The below main function is a pretty common way of executing code - put the execution into a separate code block or function.
# Note that python doesn't actually run the code all at once, it makes several passes.
# This syntax saves the execution of the code until the final pass.
# One way of reading code is to start with execution and read backwards - instead of just top-bottom, left-right.
# This often helps when troubleshooting someone else's code...
def main():
  expense_input()
  interval_input()
  age_input()
  interest_input()
  inflation_input()
  calcs()
  output()
  # GOODIE NUMBER 2: If the below argument did run, what error message would result and why?
  # After you figure it out, go ahead and remove the function call "errors(error_number)" below so your error print statements in GOODIE 1 could
  # execute appropriately (this will help in case you have problems with GOODIES 3 & 4)
  # Check out https://problemsolvingwithpython.com/07-Functions-and-Modules/07.07-Positional-and-Keyword-Arguments/
  errors(error_number)
  
# GOODIE NUMBER 3: What if you wanted to retire at a different age than 62? Can you configure a new user input to allow a different retirement age?
# GOODIE NUMBER 4: What if you wanted to specify a different Safe Withdrawal Rate other than a yearly 4%? Can you create a new input for the user to be
# able to specify a SWR?


# This statement allows python to call the main function when the script is run directly, otherwise it allows calling parts of the code indirectly. 
if __name__ == "__main__":
  main()

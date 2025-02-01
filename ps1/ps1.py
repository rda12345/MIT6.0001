#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem set 1
"""

# Part A: House Hunting
"""
annual_salary = float(input("Annual_salary: "))
portion_saved =  float(input("Portion of salary to be saved: "))
total_cost = float(input("Cost of dream home: ")) 
portion_down_payment = 0.25
current_savings = 0
r = 0.04

monthly_salary = annual_salary/12

down_payment = total_cost*portion_down_payment
monthly_money_saved = monthly_salary*portion_saved

counter = 0
while current_savings< down_payment:
    current_savings *=(1+r/12)
    current_savings += monthly_money_saved
    counter += 1
    
print("Number of months: "+ str(counter))       

"""

# Part B
"""
annual_salary = float(input("Starting annual_salary: "))
portion_saved =  float(input("Portion of salary to be saved: "))
total_cost = float(input("Cost of dream home: ")) 
semi_annual_raise = float(input("Semi annual raise: ")) 


portion_down_payment = 0.25
current_savings = 0
r = 0.04
monthly_salary = annual_salary/12
down_payment = total_cost*portion_down_payment

counter = 0
while current_savings< down_payment:
    current_savings *=(1+r/12)
    monthly_money_saved = monthly_salary*portion_saved
    current_savings += monthly_money_saved
    counter += 1
    print(counter)
    print(current_savings)
    if counter%6 == 0 :
        monthly_salary *=(1+semi_annual_raise)
print("Number of months: "+ str(counter))   
"""

#Part C

def current_saving_func(portion_saved,monthly_salary,r,current_savings,semi_annual_raise):
    """
    Input: portion_saved: Float between 0 and 1, monthly_salary: Int, r: Float
    between 0 and 1, current_savings: Int the initial current savings,
    semi_annual_raise: Float between 0 and 1.   
    Calculates the current saving after 36 months.
    """
    counter = 0
    for i in range(36):
        current_savings *=(1+r/12)
        monthly_money_saved = monthly_salary*portion_saved
        current_savings += monthly_money_saved
        counter += 1
        if counter%6 == 0 :
            monthly_salary *=(1+semi_annual_raise)
    return current_savings


#check = current_saving_func(0.4411,monthly_salary,0.04,0,0.07)
#print(check)

annual_salary = float(input("Enter the starting salary: ")) 
total_cost = 1000000
semi_annual_raise =.07
portion_down_payment = 0.25
r = 0.04
monthly_salary = annual_salary/12
down_payment = total_cost*portion_down_payment
low = 0
high = 10000
guess = (high + low)//2
init_savings = 0 
guess_down_payment = current_saving_func(0.5,monthly_salary,r,init_savings,semi_annual_raise)
steps_bisection = 1
current_savings = 0




max_portion = 1
max_savings = current_saving_func(max_portion,monthly_salary,r,current_savings,semi_annual_raise)
#print(max_savings)
if max_savings < (down_payment-100):
    print("It is not possible to pay the down payment in three years.")
else:
    #for i in range(20):
    while abs(guess_down_payment-down_payment)>=100:
        if guess_down_payment < down_payment:
            low = guess
        else: 
            high = guess
        steps_bisection +=1
        guess = (high + low)//2
        portion_saved = float(guess)/10000
        current_savings = current_saving_func(portion_saved,monthly_salary,r,init_savings,semi_annual_raise)
        guess_down_payment = current_savings 
#1500        print(current_savings)
    print("Best saving rate: ",portion_saved)
    print("Steps to bisection: ",steps_bisection) 

#This is version one of my Workout Tracker (Fit for Life) 2DIP 97/96 Assessment
#Importing required modules
import sys #Used to exit the program
import datetime #Used to validate date
#Constants
age_range=range(16,101)
workout_choices=["Athletics","Court","Field Sports","Dance","Gymnastics","Gym"]

print("Hello, Welcome to my Fit for Life (Workout Tracker) program 2026")

def user_details():
    global name, age #Stored users name and age so it can be used again in other functions to save the external file

    #Collect and validate user name input
    while True:
        name=input("Enter full name: ")
        if name.replace(" ","").isalpha(): #If name is alphabet, break the loop
            break
        elif name=="": #If name is empty, continue loop after error message
            print("Field cannot be empty")
        else:
            print("Please only enter alphabet/letters")
    #Collect and validate user age input
    while True:
        try:
            age=int(input("Enter age: "))
            #Checks whether age is in allowed range
            if age in age_range:
                break
            else:
                print("Age must be between age 16 and 100")
                sys.exit() #Exits the program
        except ValueError:
            print("The requirements for this field are that it must not be empty, must have a whole number (no decimals), and between the range of 13-100")

def present_choices():
    #Displays all the choices inside the workout_choices list
    for i in workout_choices:
        print(i)

def add_workout():
    global workout #Stores selected workout type
    global date #Stores workout date
    global reps #Stores workout reps
    print("Please pick a workout from the following: ")
    present_choices()
    
    #Validate workout selection
    while True:
        workout=input("Enter selection: ")       
        if workout=="": #If name is empty, continue loop after error message
            print("Field cannot be empty")
        elif not workout.replace(" ","").isalpha(): #If input is NOT alphabet, show error message and continue looping
            print("Please only enter alphabet/letters")
        elif workout.lower() not in [i.lower() for i in workout_choices]:#If input not a valid workout
            print("Exercise not in data base. Please select from given options")
        else:
            break
    # Source - https://stackoverflow.com/a/16870699
    # Posted by jamylak, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-05-24, License - CC BY-SA 4.0
    #Validating date using datetime module
    while True:
        date=input("Enter date (format DD/MM/YY): ")
        if date=="":
            print("Field cannot be empty.")
        else:
            try:
                datetime.datetime.strptime(date,"%d/%m/%y") #needs a comment
                break
            except ValueError:
                print("Please enter a valid date in the format DD/MM/YY")

    #Validating reps          
    while True:
        try:
            reps=int(input("Enter number of reps/distance covered: "))
            if reps<=0: #If reps are negative, invalid error message shown.
                print("Reps must be greater than zero")
            else:
                break
        except ValueError:
            print("Please enter a whole number only")
    save_score() 

def check_workout_history():
    #Reads and displays previous workout logs from extenral file
    with open ('workout_tracker_results_summary.txt','r')as file:
        contents=file.readlines() #needs a comment
        
        if len(contents)==0:
            print("This file is empty")
        else:
            print("----------------Workout History----------------")
            for line in contents:
                print(line)
    print(f"Thank you {name} for visiting! Have a nice day! 😃")
    
def save_score():
    #Saving the results to an external file for record keeping
    with open ('workout_tracker_results_summary.txt','a')as file:
        file.write(f'{name.title()} : Age {age} : {workout} : {date} : Reps {reps}\n')
    print(f"Thank you {name.title()} for visiting! Your log has been saved. Have a nice day! 😃")




#Main code 
user_details()
#Allows user to chose between logging a workout or viewiing history
log_or_history=input("Would you like to add a new log or check history? ('Log' or 'History') ('L' or 'H'): ")
if log_or_history.lower()=="l" or log_or_history.lower()=="log":
    add_workout()
else:
    check_workout_history()

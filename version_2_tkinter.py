#This is version two of my Workout Tracker (Fit for Life) 2DIP 97/96 Assessment
#It is a tkinter version

#Importing required modules
import tkinter as tk #Used for GUI
from datetime import datetime #Used for validating date input 

#Constants
#IDs are a new addition to this version, they will be used for user...Dictionary
id={23335:{"Khushi": 16},
    23336:{"Jade":23},
    23337:{"Roe":61},
    23338:{"Liam":19},
    23325:{"Nathan":37}}

#List of valid choices the user can choose from
workout_choices=["Athletics","Court","Field Sports","Dance","Gymnastics","Gym"]

#Set up
#Creating main application window
root=tk.Tk()
root.title("Fit for Life (Workout Tracker)")
root.geometry("600x800")

#Adding a scrollable_frame to allow the interface to scroll when content exceeds window limit
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame = tk.Frame(canvas)

canvas.create_window((300, 0), window=scrollable_frame, anchor="n")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

#Instructions
title=tk.Label(scrollable_frame, text="Welcome to my Fit for Life (Workout Tracker) program 2026",font=("TkDefaultFont", 15, "bold"))
title.pack()
#Instructions explaining the programs purpose and functionality
instructions=tk.Label(scrollable_frame, text="This program is a fitness tracker.\nYou can log in using your existing ID or create one.\nAdditionally you can create logs for your workout sessions, or check your history of workouts.")
instructions.pack()

#Asking ID
#Prompt user to enter an existing ID or to create a new one.
tk.Label(scrollable_frame, text="Enter ID or '0' for no ID: ").pack()

entry_id=tk.Entry(scrollable_frame) #Entry box for user to enter answer.
entry_id.pack()

def id_validation():
    global name #Storing name, age, new_id variables to be used again later
    global age
    global new_id
    try:
        ID_num=int(entry_id.get())
        if ID_num==0: #Create ID
            tk.Label(scrollable_frame, text="To make a new ID, enter the following: ").pack()
            tk.Button(scrollable_frame, text="Create ID", relief="raised", borderwidth=5, command=create_id).pack()
        elif  ID_num not in id: #Invalid
            tk.Label(scrollable_frame, text="Not valid ID").pack()
        else: #Valid ID
            name = list(id[ID_num].keys())[0]
            age = list(id[ID_num].values())[0]
            tk.Label(scrollable_frame, text="Valid ID").pack()
            new_id=ID_num
            #Proceed to main meny options
            ask_option()
    except ValueError:
        #Handles empty or non-integer input
        tk.Label(scrollable_frame, text="Please enter integers/Field cannot be empty").pack()
        
#Button triggers ID validation proccess
tk.Button(scrollable_frame,text="Enter ID", command = id_validation).pack()


#------------------------------------Creating ID functions------------------------------------

def name_validation():
    global name
    name=entry_name.get() #Stores the users input as entry_name is only the widget.
    if name=="": #If name is empty, continue loop after error message
        tk.Label(scrollable_frame, text="Field cannot be empty").pack()
        return False #Boolean to check whether name field is valid for later
    elif name.replace(" ","").isalpha(): #If name is alphabet, break the loop
        tk.Label(scrollable_frame, text="Valid Name").pack()
        return True
    else:
        tk.Label(scrollable_frame, text="Please only enter alphabet/letters").pack()
        return False

def age_validation():
    global age
    age=entry_age.get()
    if age=="": #If age is empty, continue loop after error message
        tk.Label(scrollable_frame, text="Field cannot be empty").pack()
        return False
    elif age.replace(" ","").isalpha():
        tk.Label(scrollable_frame, text="Alphabet/letters not allowed. Please enter integers/whole numbers only.").pack()
        return False
    else:
        tk.Label(scrollable_frame, text="Valid Age").pack()
        return True

def create_id():
    global entry_name
    global entry_age
    
    #Ask Name
    tk.Label(scrollable_frame, text="Enter name: ").pack()
    entry_name=tk.Entry(scrollable_frame)
    entry_name.pack()
    #Button triggers validation
    tk.Button(scrollable_frame,text="Enter Name", command = name_validation).pack()

    #Ask Age
    tk.Label(scrollable_frame, text="Enter age: ").pack()
    entry_age=tk.Entry(scrollable_frame)
    entry_age.pack()
     #Button triggers validation
    tk.Button(scrollable_frame,text="Enter Age", command = age_validation).pack()

    #Generate new ID
    tk.Button(scrollable_frame,text="Generate ID", command=generate_id).pack()

def generate_id():
    global new_id
    #If the name and age validation return true, then valid inputs have been entered.
    if name_validation() == True and age_validation() == True:
        new_id=max(id.keys())+1 #Formula to produce new_id
        id[new_id]={name:int(age)}
        tk.Label(scrollable_frame,text=f"Your new ID is {new_id}").pack()
        #Continuing to main code asking whether the user would like to create a new log or check history
        ask_option()
    else:
        tk.Label(scrollable_frame,text="Please fix errors above").pack()
        
#Asking the workout
def ask_option():
    tk.Label(scrollable_frame, text="What would you like to do?").pack()
    #Each respective button triggers the command for each function, to create an ID or to check history
    tk.Button(scrollable_frame, text="Create Workout Log", command=workout_log).pack()
    tk.Button(scrollable_frame, text="Check Workout History", command=check_history).pack()

def validate_date():
    date_text = entry_date.get()
    
    try:
        date = datetime.strptime(date_text, "%d/%m/%y") #add comment
        if date>datetime.now(): #If date entered is past today, it is in the future and thus invalid.
            tk.Label(scrollable_frame, text=f"Date cannot be in the future").pack()
        else:
            tk.Label(scrollable_frame, text=f"Valid date: {date}").pack()
    except ValueError:
        tk.Label(scrollable_frame, text="Invalid date format").pack()

def validate_reps():
    reps_text = entry_rep.get()
    try:
        reps_text=int(reps_text)
        tk.Label(scrollable_frame, text="Valid Reps").pack()
        save_workout() #Calls save workout function

    except ValueError:
        tk.Label(scrollable_frame, text="Invalid Reps format").pack()
        

#Creating Log
def workout_log():
    global entry_date
    global entry_rep
    global workout_var 
    #Ask Workout
    tk.Label(scrollable_frame, text="Select workout").pack()

    #Creating a dropdwon meny
    workout_var = tk.StringVar(scrollable_frame)
    workout_var.set(workout_choices[0]) #Sets automatic selection as the first choice in the list of workout_choices (which would be 'Athletics' in this case).
    tk.OptionMenu(scrollable_frame, workout_var, *workout_choices).pack()#add comment

    #Enter Date
    tk.Label(scrollable_frame, text="Enter Date (DD/MM/YY)").pack()
    entry_date = tk.Entry(scrollable_frame)
    entry_date.pack()
    tk.Button(scrollable_frame, text="Save", command=validate_date).pack()
    #Enter number of reps/distance covered
    tk.Label(scrollable_frame, text="Enter reps/distance covered").pack()
    entry_rep = tk.Entry(scrollable_frame)
    entry_rep.pack()
    tk.Button(scrollable_frame, text="Save", command=validate_reps).pack()
    

def save_workout():
    #Saving the results to an external file for long term storage
    with open ('version_2_workout_tracker_results_summary.txt','a')as file:
        file.write(f'{new_id}: {name.title()} : Age {age} : {workout_var.get()} : {entry_date.get()} : Reps {entry_rep.get()}\n')
    tk.Label(scrollable_frame, text=f"Thank you {name.title()} for visiting! Your log has been saved. Have a nice day! 😃").pack()
    
#Checking history
def check_history():
    #Displays only logs to the currently logged-in user ID.
    #Reads the external file to extract information
    with open ('version_2_workout_tracker_results_summary.txt','r')as file:
        contents=file.readlines()
        if len(contents)==0: #If length of contents is zero, it is empty.
            tk.Label(scrollable_frame, text="This file is empty").pack()
        else:
            tk.Label(scrollable_frame, text="----------------Workout History----------------").pack()
            for line in contents:
                #Only displaying users own history for privacy.
                if str(new_id) in line:   
                    tk.Label(scrollable_frame, text=line).pack()
                
    tk.Label(scrollable_frame, text=f"Thank you {name.title()} for visiting! Your log has been saved. Have a nice day! 😃").pack()


#Exit Button
btn = tk.Button(scrollable_frame, text="Exit", command=root.destroy)
btn.pack(side="bottom")

root.mainloop()



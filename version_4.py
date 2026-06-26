#This is version four of my Workout Tracker (Fit for Life) 2DIP 97/96 Assessment
#It is a tkinter version
#Importing required modules
import tkinter as tk #Used for GUI
from datetime import datetime #Used for validating date input 
from tkcalendar import DateEntry #Calendar widget used for date selection
import matplotlib.pyplot as plt #Graphing library


#Constants
#Dictionary that stores uer IDs, names and ages loaded from an external file
id = {}

# Reads saved user IDs from an external text file when the program starts
with open("id_dictionary.txt", "r") as file:
    for line in file: #Starts a loop
        user_id, user_name, user_age = line.strip().split(",")#Assigns the variables to string in the external file
        id[int(user_id)] = {user_name: int(user_age)} #Adds to dictionary

#List of workout choices for the dropdown bar
workout_choices=["Athletics","Court/Field Sports","Dance/Gymnastics","Gym/Personal Program", "Martial Arts/Self Defense", "Outdoor Recreation", "Snow/Winter activities", "Water sports"]

#Variable of instructions to display to the user NOT a list
HOME_INSTRUCTIONS = (
    "This program is a fitness tracker.\n"
    "You can log in using your existing ID or create one.\n"
    "Additionally you can create logs for your workout sessions, or check your history of workouts."
)

age_range=range(16,101) #Accepted age range from 16-100 inclusive

dropdown_reps=["Distance - km","No. of Reps"]

# -------------------- GUI SETUP --------------------
root=tk.Tk()
root.title("Fit for Life (Workout Tracker)")
root.geometry("950x800")
root.option_add('*Label.Background', 'lightblue') #add commetn
root.configure(bg="lightblue")

#LIGHTBLUE FRAMES CREATION
canvas = tk.Canvas(root, bg="lightblue")
scrollable_frame = tk.Frame(canvas, bg="lightblue")
user_details_frame = tk.Frame(scrollable_frame, bg="lightblue")
workout_log_frame = tk.Frame(scrollable_frame, bg="lightblue")
check_history_frame = tk.Frame(scrollable_frame, bg="lightblue")
photo_frame = tk.Frame(scrollable_frame)

#Adding a scrollable_frame so content remains accessible even if page exceeds visible window size
'''A Canvas is a container that allows widgets to become scrollable. Frames by themselves cannot be scrolled,
so I placed my frame inside a Canvas and attached a Scrollbar to the Canvas.
As more widgets are added, the Canvas allows the user to scroll up and down to see all the content.'''

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) #Packs it on the left, stretches it vertically and horizontally, and it can expand to suit the window

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)#Scrollbar created, oritented vertically and connects it to the canvas
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set) #Connects the scrollbar to the canvas, so if the canvas moves the scrollbar alters its position

canvas.create_window((475, 0), window=scrollable_frame, anchor="n")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


#Photos
#Here I am creating the tk widget as a photo, and then packing it into a label to be displayed. The photoimage is only an object not a widget thus cannot be displayed.
image_swimming = tk.PhotoImage(file="swimming_image_resized_300x300.png")
label_swimming=tk.Label(photo_frame, image=image_swimming).pack(side="left")

image_soccer = tk.PhotoImage(file="soccor_image_resized_300x300.png")
label_soccer=tk.Label(photo_frame, image=image_soccer).pack(side="left")

image_gym = tk.PhotoImage(file="gym_image_resized_300x300.png")
label_gym=tk.Label(photo_frame, image=image_gym).pack(side="left")

#Validates whether the entered ID exists or whether the user wishes to create a new account
def id_validation():
    global name #Stores variables to allow me to call these variables later in other functions
    global age
    global new_id
    try: #Validation for the integer
        ID_num=int(entry_id.get())
        if ID_num==0: #User selected to create a new ID
            id_label.config(text="To create a new ID, enter the following: ")
            create_id()
        elif  ID_num not in id: #User entered invalid ID
            id_label.config(text=(f"Sorry, {ID_num} is not a valid ID"))
        else: #User entered valid existing ID, retrieving stored details to be used later to save workout
            name = list(id[ID_num].keys())[0] #Retrieve name
            age = list(id[ID_num].values())[0] #Retrieve age
            new_id=ID_num #Retrieve ID
            ask_option()
    except ValueError:
        id_label.config(text="Please enter integers/Field cannot be empty")

#Creating ID
#Validation for name
def name_validation():
    global name
    name=entry_name.get() #Retrieves the users entered name, .get() must be used because entry_name is the widget.
    #I have created a new variable for this instead of using .get() everywhere so that the same variable (name) can be used for both new users and existing users.
    if name=="": #If name is empty, continue loop after error message
        name_label.config(text="Field cannot be empty") #configuring the error label/message
        return False
    elif name.replace(" ","").isalpha(): #If name is alphabet, return true which will allow the code to continue onto the next function
        return True
    else:
        name_label.config(text=(f"Please only enter alphabet/letters. {name} is invalid."))
        return False #returning false doesn't allow the code to move on, thus user will have to keep entering until a valid input is entered

def age_validation():
    global age
    age=entry_age.get()
    if age=="": #If name is empty, continue loop after error message
        age_label.config(text="Field cannot be empty")
        return False
    elif not age.isdigit():
        age_label.config(text=f"Please enter whole numbers only. {age} is not a whole number.")
        return False
    elif int(age) in age_range:
        return True
    else:
        age_label.config(text=(f"Age range is from 16 to 100. Sorry {age} does not fit in given range."))
        return False

    age_range = range(16, 101)




def create_id():
    global entry_name
    global entry_age
    global name_label
    global age_label
    
    #Ask Name
    tk.Label(user_details_frame, text="Enter name: ").pack()
    entry_name=tk.Entry(user_details_frame)
    entry_name.pack()
    name_label=tk.Label(user_details_frame, text="")
    name_label.pack()

    #Ask Age
    tk.Label(user_details_frame, text="Enter age: ").pack()
    entry_age=tk.Entry(user_details_frame)
    entry_age.pack()
    age_label=tk.Label(user_details_frame, text="")
    age_label.pack()

    #Calling the generate ID function which will generate and ID if inputs are valid
    tk.Button(user_details_frame,text="Generate ID",  relief="raised", bg="lightblue", command=generate_id).pack()

def generate_id():
    global new_id
    if name_validation() == True and age_validation() == True: #I have coded these variables to only be true if valid.
        new_id=max(id.keys())+1 #Formula to produce new_id
        id[new_id]={name:int(age)}
        with open("id_dictionary.txt", "a") as file:
            file.write(f"{new_id},{name.title()},{age}\n")
        tk.Label(user_details_frame,text=f"Your new ID is {new_id}").pack()
        #Continuing to main code asking whether the user would like to create a new log or check history
        ask_option()
        
#Asking the workout
def ask_option():
    tk.Label(user_details_frame, text="What would you like to do?").pack()
    #Each respective button triggers the command for each function, to create an ID or to check history
    tk.Button(user_details_frame, text="Create Workout Log",  relief="raised", bg="lightblue", command=workout_log).pack()
    tk.Button(user_details_frame, text="Check Workout History",  relief="raised", bg="lightblue", command=check_history).pack()

#Creating Log
def validate_reps():
    global reps_text
    reps_text = entry_rep.get()
    try:
        reps_text=int(reps_text)
        if reps_text>0:
            reps_label.config(text="")
            return True
        else:
            reps_label.config(text="Reps must be greater than 0")
            return False
    except ValueError:
        reps_label.config(text=f"Sorry {reps_text} is an invalid Reps format. Only integers/numbers allowed.")
        return False

def validate_date():
    if entry_date.get_date() > datetime.now().date():#If date entered is past today, it is in the future and thus invalid.
        date_label.config(text=(f"Sorry, {entry_date.get()} is in the future. Date cannot be in future."))
        return False
    else:
        date_label.config(text="")
        return True

def workout_log():    
    global entry_date
    global entry_rep
    global workout_var
    global date_label
    global reps_label
    global reps_var
    
    #Ask Workout
    '''I delete all the widgets because I encountered an error in which when user comes back to the workout webpage,
    the widgets get created again so I would have 2x labels 2x entry boxes, thus everytime this function is called I
    delete everything so that the brand new widgets can be displayed without any stack ups'''
    for widget in workout_log_frame.winfo_children():
        widget.destroy()
    #Configuring the instructions tailored to this webpage
    instructions.config(text="This webpage is designed to save your new workout log. Please select the activity you did, the date and the number of sets. Thank you!")
    user_details_frame.pack_forget() #Remove the user_details frame, display the workout_log_frame.
    workout_log_frame.pack()

    #Enter workout
    tk.Label(workout_log_frame, text="Select workout: ").grid(row=0, column=0)
    #Drop down bar being created in the workout log frame
    workout_var = tk.StringVar(workout_log_frame) #add comment
    workout_var.set(workout_choices[0]) #Setting the initial dropdown as the first workout in the workout_choices list which is 'Atheltics'
    tk.OptionMenu(workout_log_frame, workout_var, *workout_choices).grid(row=0, column=1)
    
    #Enter Date
    #Retrieved online, refrecnes on word document
    tk.Label(workout_log_frame, text="Enter Date (DD/MM/YY): ").grid(row=1, column=0)
    entry_date = DateEntry(workout_log_frame, date_pattern="yyyy-mm-dd") #add comment
    entry_date.grid(row=1, column=1)
    date_label=tk.Label(workout_log_frame, text="")
    
    #Enter number of reps/distance covered
    tk.Label(workout_log_frame, text="Enter reps/distance covered: ").grid(row=2, column=0)
    entry_rep = tk.Entry(workout_log_frame)
    entry_rep.grid(row=2, column=1)
    reps_label=tk.Label(workout_log_frame, text="")
    
    reps_var = tk.StringVar(workout_log_frame)
    reps_var.set(dropdown_reps[0])
    tk.OptionMenu(workout_log_frame, reps_var, *dropdown_reps).grid(row=3, column=1)

    tk.Button(workout_log_frame, text="Save",  font=("TkDefaultFont", 10, "bold"), relief="raised", bg="lightblue", command=lambda: (validate_date(), validate_reps(), save_workout())).grid(row=4, column=0, columnspan=2, pady=20)
    date_label.grid(row=5, column=0, columnspan=2)#Works as spacing if the input is valid, displays error message if input is invalid
    reps_label.grid(row=6, column=0, columnspan=2) 
    
    tk.Button(workout_log_frame, text="Return to homescreen",  relief="raised", bg="lightblue", command=lambda: (workout_log_frame.pack_forget(), instructions.config(text=HOME_INSTRUCTIONS), user_details_frame.pack())).grid(row=8, column=0, columnspan=2)
    

def save_workout():
    #Saving the results to an external file as it may come in use later
    if validate_date()==True and validate_reps()==True:
        with open ('version_4.txt','a')as file:
            file.write(f'{new_id}: {name.title()} : Age {age} : {workout_var.get()} : {entry_date.get()} : Reps {entry_rep.get()} ({reps_var.get()})\n')
        date_label.config(text=f"Thank you {name.title()} for visiting! Your log has been saved. Have a nice day! 😃")
    
#Checking history
def graph():
    dates = []
    reps = []

    with open("version_4.txt", "r") as file:
        for line in file:
            data = line.strip().split(":")

            # Only current user
            if str(new_id) != data[0].strip():
                continue

            # Convert date from YYYY-MM-DD format
            date = datetime.strptime(data[4].strip(), "%Y-%m-%d")

            # Get number of reps
            rep = int(data[5].strip().split()[1])

            dates.append(date)
            reps.append(rep)

    if len(dates) == 0:
        tk.Label(check_history_frame, text="No data to graph yet").pack()
        return

    plt.figure(figsize=(12, 5))
    plt.plot(dates, reps, marker="o")
    plt.title(f"{name.title()}'s Workout Progress Over Time")
    plt.xlabel("Date")
    plt.ylabel("Reps")
    plt.grid(True)
    plt.show()
    
def check_history():
    #Ensuring double ups do not get displayed since everytime function is called new widgets are made, so it is important to delete the older widgets
    for widget in check_history_frame.winfo_children():
        widget.destroy()
    user_details_frame.pack_forget()
    #Display check_histroy_frame and forget the user_details_frame
    check_history_frame.pack()
    instructions.config(text="This webpage is designed to check your workout history.")
    with open ('version_4.txt','r')as file:
        contents=file.readlines()
    if len(contents)==0: #If the content is empty, display error message
        tk.Label(check_history_frame, text="This file is empty").pack()
    else:
        found=False
        tk.Label(check_history_frame, text="------------------------------Workout History------------------------------").pack()
        for line in contents:
            if str(new_id) in line:
                tk.Label(check_history_frame, text=line).pack()
                found=True
        if found==False:
            tk.Label(check_history_frame, text="Sorry, no logs created yet.").pack()
            
    tk.Label(check_history_frame, text=f"Thank you {name.title()} for visiting! Have a nice day! 😃").pack()
    tk.Button(check_history_frame, text="Graph",  relief="raised", bg="lightblue", command=graph).pack()
    tk.Button(check_history_frame, text="Return to homescreen",  relief="raised", bg="lightblue", command=lambda: (check_history_frame.pack_forget(), instructions.config(text=HOME_INSTRUCTIONS), user_details_frame.pack())).pack(pady=10)

#-----------------------------------------MAIN CODE-----------------------------------------
#Instructions
#Frame user details
title=tk.Label(scrollable_frame, text="Fit for Life (Workout Tracker) program 2026",font=("TkDefaultFont", 30, "bold"))
title.pack(pady=7)
instructions=tk.Label(scrollable_frame, text=HOME_INSTRUCTIONS)
instructions.pack(pady=10)

photo_frame.pack()

#Asking ID starts the whole code.
tk.Label(user_details_frame, text="Enter ID or '0' for create ID: ").pack()

entry_id=tk.Entry(user_details_frame)
entry_id.pack()

#ID Label is the label I will use for error messages by configuring it later, currently it is empty and used to make a gap/for aesthetic purposes
id_label=tk.Label(user_details_frame, text="")
id_label.pack()

ID_Button=tk.Button(user_details_frame,text="Enter ID", relief="raised", bg="lightblue", command = id_validation)
ID_Button.pack()

user_details_frame.pack()

#Exit Button
exit_btn = tk.Button(scrollable_frame, text="Exit",  relief="raised", bg="lightblue", command=root.destroy)
exit_btn.pack(side="bottom")

root.mainloop()

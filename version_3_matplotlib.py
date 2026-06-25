#This is version three of my Workout Tracker (Fit for Life) 2DIP 97/96 Assessment
#It is a tkinter version ADD MORE COMMENT ON INTO HERE ON THE TOP
#Importing required modules
import tkinter as tk #Used for GUI
from datetime import datetime #Used for validating date input 
from tkcalendar import DateEntry #Calendar widget used for date selectio

#Constants
#Dictionary that stores uer IDs, names and ages loaded from an external file
id = {}

# Reads saved user IDs from an external text file when the program starts
with open("id_dictionary.txt", "r") as file:
    for line in file:
        user_id, user_name, user_age = line.strip().split(",")
        id[int(user_id)] = {user_name: int(user_age)}

#List of workout choices for the dropdown bar
workout_choices=["Athletics","Court/Field Sports","Dance/Gymnastics","Gym/Personal Program", "Martial Arts/Self Defense", "Outdoor Recreation", "Snow/Winter activities", "Water sports"]

#List of instructions to display to the user
HOME_INSTRUCTIONS = (
    "This program is a fitness tracker.\n"
    "You can log in using your existing ID or create one.\n"
    "Additionally you can create logs for your workout sessions, or check your history of workouts."
)

age_range=range(16,101) #Accepted age range from 16-100 inclusive

# -------------------- GUI SETUP --------------------
root=tk.Tk()
root.title("Fit for Life (Workout Tracker)")
root.geometry("950x800")

#Adding a scrollable_frame so content remains accessible even if page exceeds visible window size
canvas = tk.Canvas(root) #ADD COMMENTS FOR THIS PART
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame = tk.Frame(canvas)

canvas.create_window((475, 0), window=scrollable_frame, anchor="n")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

#Instructions
#Frame user details
user_details_frame=tk.Frame(scrollable_frame)

title=tk.Label(scrollable_frame, text="Welcome to my Fit for Life (Workout Tracker) program 2026",font=("TkDefaultFont", 30, "bold"))
title.pack(pady=7)
instructions=tk.Label(scrollable_frame, text=HOME_INSTRUCTIONS)
instructions.pack(pady=10)

#Photos Frame
photo_frame=tk.Frame(scrollable_frame)

#Photos
#Here I am creating the tk widget as a photo, and then packing it into a label to be displayed
image_swimming = tk.PhotoImage(file="swimming_image_resized_300x300.png")
label_swimming=tk.Label(photo_frame, image=image_swimming).pack(side="left")

image_soccer = tk.PhotoImage(file="soccor_image_resized_300x300.png")
label_soccer=tk.Label(photo_frame, image=image_soccer).pack(side="left")

image_gym = tk.PhotoImage(file="gym_image_resized_300x300.png")
label_gym=tk.Label(photo_frame, image=image_gym).pack(side="left")

photo_frame.pack()

#Asking ID starts the whole code.
tk.Label(user_details_frame, text="Enter ID or '0' for create ID: ").pack()

entry_id=tk.Entry(user_details_frame)
entry_id.pack()

#ID Label is the label I will use for error messages by configuring it later, currently it is empty and used to make a gap/for aesthetic purposes
id_label=tk.Label(user_details_frame, text="")
id_label.pack()

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
            id_label.config(text="Not valid ID")
        else: #User entered valid existing ID, retrieving stored details to be used later to save workout
            name = list(id[ID_num].keys())[0] #Retrieve name
            age = list(id[ID_num].values())[0] #Retrieve age
            new_id=ID_num  #Retrieve ID
            ask_option()
    except ValueError:
        id_label.config(text="Please enter integers/Field cannot be empty")
ID_Button=tk.Button(user_details_frame,text="Enter ID", relief="raised", bg="lightblue", command = id_validation)
ID_Button.pack()

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
        name_label.config(text="Please only enter alphabet/letters")
        return False #returning false doesn't allow the code to move on, thus user will have to keep entering until a valid input is entered

def age_validation():
    global age
    age=entry_age.get()
    if age=="": 
        age_label.config(text="Field cannot be empty")
        return False
    elif age.replace(" ","").isalpha(): #If age is alphabet, invalid.
        age_label.config(text="Alphabet/letters not allowed. Please enter integers/whole numbers only.")
        return False
    elif int(age) in age_range:
        return True
    else:
        age_label.config(text=(f"Age range is from 16 to 100. Sorry {age} does not fit in given range.")) #Personalised age error message
        return False

def create_id():
    global entry_name
    global entry_age
    global name_label
    global age_label
    
    #Asking Name
    tk.Label(user_details_frame, text="Enter name: ").pack()
    entry_name=tk.Entry(user_details_frame)
    entry_name.pack()
    name_label=tk.Label(user_details_frame, text="")
    name_label.pack()

    #Asking Age
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

user_details_frame.pack()

#Creating Log
#Frame
workout_log_frame=tk.Frame(scrollable_frame)

def validate_reps():
    global reps_text
    reps_text = entry_rep.get()
    try:
        reps_text=int(reps_text)
        if reps_text>0:
            reps_label.destroy()
            return True
        else:
            reps_label.config(text="Reps must be greater than 0")
            return False
    except ValueError:
        reps_label.config(text="Invalid Reps format")
        return False

def validate_date():
    if entry_date.get_date() > datetime.now().date():#If date entered is past today, it is in the future and thus invalid.
        date_label.config(text="Date cannot be in future")
        return False
    else:
        date_label.destroy()
        return True

def workout_log():    
    global entry_date
    global entry_rep
    global workout_var
    global date_label
    global reps_label
    
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
    tk.Label(workout_log_frame, text="Select workout").pack()
    #Drop down bar being created in the workout log frame
    workout_var = tk.StringVar(workout_log_frame) #add comment
    workout_var.set(workout_choices[0]) #Setting the initial dropdown as the first workout in the workout_choices list which is 'Atheltics'
    tk.OptionMenu(workout_log_frame, workout_var, *workout_choices).pack() #add comment
    
    #Enter Date
    tk.Label(workout_log_frame, text="Enter Date (DD/MM/YY): ").pack()
    entry_date = DateEntry(workout_log_frame, date_pattern="yyyy-mm-dd") #add comment
    entry_date.pack()
    date_label=tk.Label(workout_log_frame, text="")
    
    #Enter number of reps/distance covered
    tk.Label(workout_log_frame, text="Enter reps/distance covered").pack()
    entry_rep = tk.Entry(workout_log_frame)
    entry_rep.pack()
    reps_label=tk.Label(workout_log_frame, text="")

    
    tk.Button(workout_log_frame, text="Save",  relief="raised", bg="lightblue", command=lambda: (validate_date(), validate_reps(), save_workout())).pack()
    date_label.pack() #Works as spacing if the input is valid, displays error message if input is invalid
    reps_label.pack()
    
    tk.Button(workout_log_frame, text="Return to homescreen",  relief="raised", bg="lightblue", command=lambda: (workout_log_frame.pack_forget(), instructions.config(text=HOME_INSTRUCTIONS), user_details_frame.pack())).pack(side="bottom")
    

def save_workout():
    #Saving the results to an external file as it may come in use later
    if validate_date()==True and validate_reps()==True:
        with open ('version_3_workout_tracker_results_summary.txt','a')as file:
            file.write(f'{new_id}: {name.title()} : Age {age} : {workout_var.get()} : {entry_date.get()} : Reps {entry_rep.get()}\n')
        tk.Label(workout_log_frame, text=f"Thank you {name.title()} for visiting! Your log has been saved. Have a nice day! 😃").pack()

#Checking history
#History frame
check_history_frame=tk.Frame(scrollable_frame)

def check_history():
    #Ensuring double ups do not get displayed since everytime function is called new widgets are made, so it is important to delete the older widgets
    for widget in check_history_frame.winfo_children():
        widget.destroy()
    user_details_frame.pack_forget()
    #Display check_histroy_frame and forget the user_details_frame
    check_history_frame.pack() 
    instructions.config(text="This webpage is designed to check your workout history.")
    with open ('version_3_workout_tracker_results_summary.txt','r')as file:
        contents=file.readlines()
        if len(contents)==0: #If the content is empty, display error message
            tk.Label(check_history_frame, text="This file is empty").pack()
        else:
            tk.Label(check_history_frame, text="------------------------------Workout History------------------------------").pack()
            for line in contents:
                if str(new_id) in line:   
                    tk.Label(check_history_frame, text=line).pack()
                
    tk.Label(check_history_frame, text=f"Thank you {name.title()} for visiting! Have a nice day! 😃").pack()
    tk.Button(check_history_frame, text="Return to homescreen",  relief="raised", bg="lightblue", command=lambda: (check_history_frame.pack_forget(), instructions.config(text=HOME_INSTRUCTIONS), user_details_frame.pack())).pack()

#Exit Button
btn = tk.Button(scrollable_frame, text="Exit",  relief="raised", bg="lightblue", command=root.destroy) #Will destroy the root window which contains everything
btn.pack(side="bottom")

root.mainloop()

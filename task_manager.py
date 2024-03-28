# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# ========= importing libraries ==========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

dictionary_components_list = ['username','title','description','due_date','assigned_date','completed']
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)


# ======== Login Section ========
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")


# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# ========= Defining functions for future use  =========

# --------- Function for registering users ---------
def reg_user(): 
      new_username = input("New Username: ")
      if new_username == username:
            print("That user already exists. Please try again")
            new_username = input("New Username: ")
            if new_username == username:
                print("Invalid Username.")
                exit()
      new_password = input("New Password: ")
      confirm_password = input("Confirm Password: ")
      if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
      else:
            print("Passwords do no match")

# --------- Function for adding tasks ---------
            
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
    new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# --------- Function for printing all tasks to the terminal ---------
def view_all():
    print("\n")
    for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

# --------- Function for viewing and editing all tasks assigned to the current user ---------
            
def view_mine():
    
        task_selection_list_for_operation = []
        list_of_assigned_tasks = []
        counter_for_assigned_tasks = 0
        for t in task_list:
            if t['username'] == curr_user:
                counter_for_assigned_tasks+=1
                disp_str = f"Task {counter_for_assigned_tasks}: \t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
                task_selection_list_for_operation.append(disp_str)
                list_of_assigned_tasks.append(t)
        
        task_selection = int(input("Enter the number of a task to edit or mark as complete, or enter '-1' to return to the main menu:\n "))
        if task_selection == int(-1):
         print(menu)
        else:
            user_selected_option = int(task_selection - int(1))
            if user_selected_option >= len(task_selection_list_for_operation):
                print("That task does not exist.")
                exit()
            else:
             print("\n")
             print(task_selection_list_for_operation[user_selected_option])
             print("\n")
             edit_or_complete_input = input("Would you like to edit this task ('e'), or mark as completed ('c')? \n")
             if edit_or_complete_input.lower() == 'e':
                        with open("tasks.txt", 'r') as task_file:
                              task_data = task_file.read().split("\n") 
                              for t in task_data:
                                   edit_selected_task = task_data[user_selected_option]
                                   edit_task_components = edit_selected_task.split(";")
                                   if edit_task_components[5] == "Yes":
                                        print("This task has already been completed.")
                                        exit()   
                        username_or_due_date = input("Would you like to change the username ('u') or due date ('d')? ")
                        if username_or_due_date.lower() == 'u':
                         with open("tasks.txt", 'r') as task_file:
                              task_data = task_file.read().split("\n")
                              edit_selected_task = task_data[user_selected_option]
                              edit_task_components = edit_selected_task.split(";")
                              changed_username = input("Change the name of person assigned to task: ")
                              edit_task_components[0] = changed_username
                              task_data[user_selected_option] = ";".join(edit_task_components)
                        with open("tasks.txt", "w") as task_file:
                         for t in task_data:
                             task_list_str = str(t)
                             task_file.write(task_list_str)
                             task_file.write("\n")
                         if username_or_due_date == 'd':
                          with open("tasks.txt", 'r') as task_file:
                           task_data = task_file.read().split("\n")
                           edit_selected_task = task_data[user_selected_option]
                           edit_task_components = edit_selected_task.split(";")
                           task_due_date = input("Due date of task (YYYY-MM-DD): ")
                           edit_task_components[3] = task_due_date
                           task_data[user_selected_option] = ";".join(edit_task_components)
                           with open("tasks.txt", "w") as task_file:
                            for t in task_data:
                             task_list_str = str(t)
                             task_file.write(task_list_str)
                             task_file.write("\n")
                 

             if edit_or_complete_input.lower() == 'c':
              with open("tasks.txt", 'r') as task_file:
               task_data = task_file.read().split("\n")
              list_to_edit_task_components = []
              for t in task_data:
                edit_task_components = t.split(';')
                list_to_edit_task_components.append(edit_task_components)
              edit_task_components_list_for_user = [e for e in list_to_edit_task_components if e[0] == curr_user]
              task_selected_to_complete = edit_task_components_list_for_user[user_selected_option]
              task_selected_to_complete[5] = 'Yes'
              for e in list_to_edit_task_components:
                  if e[2] == task_selected_to_complete[2]:
                    e = task_selected_to_complete
              with open("tasks.txt", "w") as task_file:
                         for e in list_to_edit_task_components:
                             joined_tasks = ";".join(e)
                             str_joined_tasks = str(joined_tasks)
                             task_file.write(str_joined_tasks)
                             task_file.write("\n")
            print("\n", "Task completed.")               
# --------- Function for generating reports ---------
                             
def generate_reports():
        with open("tasks.txt", 'r') as task_file:
         task_data = task_file.read().split("\n")
         joined_tasks = ";".join(task_data)
         full_task_list = joined_tasks.split(";")
        task_list_for_comparing_dates = []
        for t in task_data:
             task_components = t.split(";")
             task_list_for_comparing_dates.append(task_components)
        total_task_count = 0
        completed_tasks_count = 0
        incomplete_task_count = 0
        overdue_task_count = 0
        total_user_count = 0 
        # User overview report
        if not os.path.exists("User overview.txt"):
         with open("User overview.txt", "w") as user_overview_file:
          pass
        # Reading in and manipulating task data
        with open("user.txt", 'r') as user_file:
         user_data = user_file.read().split("\n")
         joined_users = ";".join(user_data)
         full_user_list = joined_users.split(";")
        for u in user_data:
            total_user_count += 1
        for t in task_data:
             total_task_count += 1
        total_users = (f"Total Users: {total_user_count}")
        task_no = (f"Total Tasks: {total_task_count}")
        with open("tasks.txt", 'r') as task_file:
          task_data = task_file.read().split("\n")
          joined_tasks = ";".join(task_data)
          full_task_list = joined_tasks.split(";")
          full_completed_tasks_dict = {}
          for f in full_user_list[::2]:
              full_completed_tasks_dict[f] = 0 
              for e in task_list_for_comparing_dates:
               if e[5] == 'Yes' and e[0] == f:
                 full_completed_tasks_dict[f] += 1
        with open("tasks.txt", 'r') as task_file:
          task_data = task_file.read().split("\n")
          joined_tasks = ";".join(task_data)
          full_task_list = joined_tasks.split(";")
          full_incomplete_tasks_dict = {}
          for f in full_user_list[::2]:
              full_incomplete_tasks_dict[f] = 0 
              for e in task_list_for_comparing_dates:
                  if e[5] == 'No' and e[0] == f:
                      full_incomplete_tasks_dict[f] += 1
        with open("tasks.txt", 'r') as task_file:
          task_data = task_file.read().split("\n")
          joined_tasks = ";".join(task_data)
          full_task_list = joined_tasks.split(";")
          overdue_tasks_dict = {}
          for f in full_user_list[::2]:
            overdue_tasks_dict[f] = 0
            for e in task_list_for_comparing_dates:
                if e[5] == 'No' and e[3] <= e[4] and e[0] == f:
                    overdue_tasks_dict[f] += 1
        with open("User overview.txt", "w") as user_overview_file:
         user_overview_file.write(total_users)
         user_overview_file.write("\n")
         user_overview_file.write(task_no)
         user_overview_file.write("\n")
         full_user_list_dict = {}
         list_of_users = [] 
         for t in full_task_list:
          for f in full_user_list[::2]:
             if t == f:
                 list_of_users.append(t)
         for f in full_user_list[::2]:
             full_user_list_dict[f] = 0
         for d in full_user_list_dict:
             for t in full_task_list:
                 if d == t:
                     full_user_list_dict[d] += 1
         for f in full_user_list[::2]:
             percentage_total_task_user = (full_user_list_dict[f]/total_task_count) * 100
             user_overview_file.write(f"{f} has {full_user_list_dict[f]} tasks assigned and {int(percentage_total_task_user)}% of the total tasks.")
             user_overview_file.write("\n")
         for f in full_user_list[::2]:
                 percentage_complete_task_user = (full_completed_tasks_dict[f]/full_user_list_dict[f]) * 100
                 user_overview_file.write(f"{int(percentage_complete_task_user)}% of {f}'s tasks are completed.")
                 user_overview_file.write("\n")
         for f in full_user_list[::2]:
                 percentage_incomplete_task_user = (full_incomplete_tasks_dict[f]/full_user_list_dict[f]) * 100
                 user_overview_file.write(f"{int(percentage_incomplete_task_user)}% of {f}'s tasks are incomplete.")
                 user_overview_file.write("\n")
         for f in full_user_list[::2]:
                percentage_overdue_task_user = (overdue_tasks_dict[f]/full_user_list_dict[f]) * 100
                user_overview_file.write(f"{int(percentage_overdue_task_user)}% of {f}'s tasks are overdue.")
                user_overview_file.write("\n")
         
        # Task overview report
        if not os.path.exists("Task overview.txt"):
         with open("Task overview.txt", "w") as task_overview_file:
          pass
        for d in task_list_for_comparing_dates:
            if d[5] == 'No' and d[3] <= d[4]:
                overdue_task_count += 1
        for f in full_task_list:
             if f == 'Yes':
                 completed_tasks_count += 1
        for f in full_task_list:
             if f == 'No':
                 incomplete_task_count += 1
        percentage_of_incomplete_tasks = (incomplete_task_count/total_task_count) * 100
        percentage_of_overdue_tasks = (overdue_task_count/total_task_count) * 100
        with open("Task overview.txt", "w") as task_overview_file:
          task_no = (f"Total Tasks: {total_task_count}")
          completed_tasks = (f"Completed Tasks: {completed_tasks_count}")
          uncompleted_tasks = (f"Uncompleted Tasks: {incomplete_task_count}")
          overdue_tasks = (f"Overdue Tasks: {overdue_task_count}")
          percentage_of_incomplete_tasks_text = (f"Percentage of Incomplete Tasks: {int(percentage_of_incomplete_tasks)}%")
          percentage_of_overdue_tasks_text = (f"Percentage of Overdue Tasks: {int(percentage_of_overdue_tasks)}%")
          task_overview_file.write(task_no)
          task_overview_file.write("\n")
          task_overview_file.write(completed_tasks) 
          task_overview_file.write("\n")
          task_overview_file.write(uncompleted_tasks)
          task_overview_file.write("\n")
          task_overview_file.write(overdue_tasks)
          task_overview_file.write("\n")
          task_overview_file.write(percentage_of_incomplete_tasks_text)
          task_overview_file.write("\n")
          task_overview_file.write(percentage_of_overdue_tasks_text)
          print('Reports Generated.')

# -----------------------------------------------------------------------------


# ========= Login input =========
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True



# ========= User Menu =========
while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports                 
ds - Display statistics
e - Exit
: ''').lower()


# --------- Menu options which call the previously defined functions ---------
    
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
        exit()
    elif menu == 'vm':
        view_mine()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    elif menu == 'gr':
        generate_reports()
        exit()
    elif menu == 'ds' and curr_user == 'admin': 
        print("\n")
        if not os.path.exists("User overview.txt"):
            generate_reports()
        
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        with open("User overview.txt", 'r') as user_overview_file:
            user_stats = user_overview_file.read().split("\n")
            joined_user_stats = " ".join(user_stats)
            split_user_stats = joined_user_stats.split()

        with open("Task overview.txt", 'r') as task_overview_file:
            task_stats = task_overview_file.read().split("\n")

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")
        print("\n")
        print("-----------------------------------")
        print("\t","User Overview")
        print("-----------------------------------")
        print("\n")
        for u in user_stats: 
            print(u,"\n")
        print("\n")
        print("-----------------------------------")
        print("\t","Task Overview")
        print("-----------------------------------")
        print("\n")
        for t in task_stats:
            print(t,"\n")
        exit()

# --------- Exception error for user menu ---------
    else:
        print("You have made a wrong choice, Please Try again")
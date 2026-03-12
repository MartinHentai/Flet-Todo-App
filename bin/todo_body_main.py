import json 
from datetime import datetime, date, timedelta
from styles import load_fonts
from dateutil.relativedelta import relativedelta, MO, SA, SU,TU, WE, TH, FR
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY
import os
import uuid
import time








def update_task_due(data_ref, task_id, date):...
def load_tasks():...
def save_tasks(tasks_json):...
def enumerate_tasks(tasks_json):...
def add_task(tasks_json, new_task):...
def show_tasks(tasks_json):...
def task_status(tasks_json, task_id, mode=True):...
def delete_task(task_id, data_ref):...
def generate_id():...
def save_to_json(data):...
def update_ram_data(data_ref, task_id, status):...
def edit_task_text(task_id, text, data_ref):...

def save_to_json(data):   
    """
    Save tasks to the JSON file.
    
    :param tasks_json: Dictionary containing tasks.
    """

    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "tasks.json")

    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as e:
            return 1, f"Error has orrured: {e}"


def update_task_due(data_ref, task_id, date):
    if data_ref:
        for task in data_ref["tasks"]:
            if task["id"] == task_id:
                task["due_date"] = date
                if not task["due_date"]:
                    task["recurrence"] = None
                break

def validate_length(P):
    MAX_CHARS = 3
    """Callback function to check the length of the pending input in entry."""
    if len(P) <= MAX_CHARS:
        return True  # Allow the change
    else:
        return False # Reject the change
    
def update_task_status(data_ref, task_id, status):

    """Updates the dictionary sitting in RAM."""
    
    if data_ref:
        for task in data_ref["tasks"]:
            if task["id"] == task_id:
                task["status"] = status
                break


def load_tasks():
    # Get the folder where logic.py is actually located
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "tasks.json")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # SUCCESS: Always return (data, error_message)
            return data, None
            
    except FileNotFoundError:
        return {"tasks": []}, "No saved tasks found. Creating new file."
        
    except json.JSONDecodeError:
        return {"tasks": []}, "Error: tasks.json is corrupted!"
    

  
    

def add_task(name, data_ref):

    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    new_task = {
        "task_name": name,
        "id": generate_id(),
        "status": 0,
        "task_date": date,
        "due_date": None,
        "recurrence": None
    }
    data_ref["tasks"].append(new_task)
    return new_task

def delete_task(task_id, data_ref):
    # Keep every task EXCEPT the one with this ID
    data_ref["tasks"] = [t for t in data_ref["tasks"] if t["id"] != task_id]

def edit_task_text(task_id, text, data_ref):

    for t in data_ref["tasks"]:
        if t["id"] == task_id:
            t["task_name"] = text


def generate_id():
    return str(uuid.uuid4())[:16] 

def get_today():
    return  date.today().strftime( "%d-%m-%Y")

def get_today_wd():
    return  date.today().weekday()


def get_tomorrow():
    return (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")

def get_yesterday():
    return (date.today() - timedelta(days=1)).strftime("%d-%m-%Y")

def get_month(date_in):
    """
    Docstring for get_month

    Returns month as locale's abbreviated name from passed date.
    
    :param date_in: string with date, date format strictly should be: "month-day-year", e.g.: "12-02-2023"

    Description: 
    """ 
    date_in = date.strptime(date_in, "%d-%m-%Y")
    return date_in.strftime("%b")



def get_weekday(date_in):
    """
    Docstring for get_weekday
    
    :param date_in: Description
    """
    
    date_in = date.strptime(date_in, "%d-%m-%Y")
    return date_in.strftime("%a")



            

def get_due_display_text(date_in):
    """
    Returns 'Today', 'Tomorrow', or the Formatted Date.
    """
    if not date_in:
        return None
        
    if date_in == get_today():
        return "Today"
    
    elif date_in == get_tomorrow():
        return "Tomorrow"
    
    elif date_in == get_yesterday():
        return "Yesterday"

    return due_for_label(date_in)


def due_for_label(date_in):
    if not date_in:
        return None

    try:
        conv_date = datetime.strptime(date_in, "%d-%m-%Y")
    except (ValueError, TypeError):
        return str(date_in)

    d = get_weekday(date_in)
    m = get_month(date_in)
    
    if conv_date.year == date.today().year:
        return f"{d}, {conv_date.day} {m}"
    
    return f"{d}, {conv_date.day} {m} {conv_date.year}"




RECUR_NAMES = {
    1: "Daily",
    2: "Weekdays",
    3: "Weekends",
    4: "Weekly",
    5: "Monthly",
    6: "Annually",
    7: "Custom weekdays"
}
RECUR_IDS = {
    "Daily": 1,
    "Weekdays": 2,
    "Weekends": 3,
    "Weekly": 4,
    "Monthly": 5,
    "Annually": 6,
    "Custom": 7
}
def set_task_recurrence(data_ref, task_id, recur_type, interval=1, weekdays_array=None):
    """
    Connects setting the rule and calculating the first occurrence.
    Saves the rule to the task dictionary in RAM (data_ref).
    """
    if recur_type not in (1,2,3,4,5,6,7) and recur_type != None:
        raise ValueError("Incorrect recurrence type")
    if interval < 1: 
        raise ValueError("Interval cannot be less than 1")
    # 1. Map the type name using the dictionary
    type_name = RECUR_NAMES.get(recur_type, "None")
    today = get_today()
    # 2. Determine the data structure to save in JSON
    if recur_type == 7:
        if not weekdays_array:
            raise ValueError("Custom weekday recurrence requires a weekdays array.")
        if any(wd < 0 or wd > 6 for wd in weekdays_array):
            raise ValueError("Weekday must be between 0 (Mon) and 6 (Sun).")
        recur_data = {
            "recurring_type": type_name, 
            "interval": interval, 
            "weekdays": weekdays_array
        }
    elif type_name == "None":
        recur_data = None    
    elif interval > 1:
        recur_data = {
            "recurring_type": type_name, 
            "interval": interval
        }
    else:
        recur_data = {
            "recurring_type": type_name, 
            "interval": None
        }

    # 3. Update the task in data_ref and calculate the next due date
    for t in data_ref["tasks"]:
        if t["id"] == task_id:
            t["recurrence"] = recur_data
            
            if recur_data == None:
                output = None
                break

            if not t["due_date"]:
                t["due_date"] = today    

            # if current task is not complete, return None.   Else, create copy of this task with new due date 
            if t["status"] == 0:
                output = None
                break                

            output = new_task_recurrence(data_ref,t,recur_type,interval,weekdays_array)
            break
    return output


def new_task_recurrence(data_ref, task, recur_type, interval=1, weekdays_array=None):
    copied_task = add_task(task["task_name"],data_ref)
    copied_task["recurrence"] = task["recurrence"]
    start_date = task["due_date"]
    if recur_type == 7:
        copied_task["due_date"] = custom_recurr_week(interval, weekdays_array, start_date)
    else:
        copied_task["due_date"] = calc_recurring(start_date, recur_type, interval)
    return copied_task


def calc_recurring(date_in, recur_type, n=1):
    """
    Efficiently calculates the next occurrence using rrule.
    Types: 1=Daily, 2=Weekdays, 3=Weekends, 4=Weekly, 5=Monthly, 6=Annually
    """
    if recur_type not in (1,2,3,4,5,6):
        raise ValueError("Incorrect recurrence type")
    # 1. Parse the anchor date
    anchor_dt = datetime.strptime(date_in, "%d-%m-%Y")

    # 2. Map recur_type to rrule parameters
    # Default settings
    byweekday = None
    freq_map = {
        1: DAILY,   # days
        2: DAILY,   # Weekdays (Mon-Fri)
        3: DAILY,   # Weekends (Sat-Sun)
        4: WEEKLY,  # weeks
        5: MONTHLY, # months
        6: YEARLY   # years
    }

    if recur_type == 2: # Weekdays (Mon-Fri)
        byweekday = (MO, TU, WE, TH, FR)
    elif recur_type == 3: # Weekends (Sat-Sun)
        byweekday = (SA, SU)

    # 3. Create the rule
    rule = rrule(
        freq=freq_map[recur_type], #
        dtstart=anchor_dt, 
        interval=n, 
        byweekday=byweekday
    )

    # 4. Find the first occurrence strictly AFTER the current time. With today included.
    today = datetime.combine(datetime.now(), datetime.min.time())
    next_occurrence = rule.after(today, inc=True)

    return next_occurrence.strftime("%d-%m-%Y")



WEEKDAYS = [MO, TU, WE, TH, FR, SA, SU]

def custom_recurr_week(n: int, day_arr: list, date_in: str):
    # 1. Parse string to datetime
    start_dt = datetime.strptime(date_in, "%d-%m-%Y")
    
    # 2. Convert [0, 2, 4] list to [MO, WE, FR]
    rrule_days = [WEEKDAYS[i] for i in day_arr]
    
    # 3. Create the rule
    # dtstart is CRITICAL: it anchors the "every n weeks" cycle
    rule = rrule(WEEKLY, interval=n, byweekday=rrule_days, dtstart=start_dt)
    
    # 4. Get today's date at midnight
    # We strip time from 'now' to compare dates fairly
    today = datetime.combine(date.today(), datetime.min.time())

    # 5. Get the next valid due date strictly after "today"
    # "inc=True" means if today is a valid due date, return today.
    next_date = rule.after(today, inc=True)
    
    if next_date:
        return next_date.strftime("%d-%m-%Y")
    return date_in





            















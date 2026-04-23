#!/bin/python3

from flask import Flask, request, redirect, url_for
from datetime import datetime, timedelta
from flask.templating import render_template
import pickle

default_muscles = ["traps", "delts", "lats", "low back", "pecs", "biceps", "triceps", "abs", "glutes", "quads", "hams", "calves"]
current_muscles = []

### Setting up objects for tracking muscle soreness
class Muscle():

    """
    Muscle class for tracking soreness 
    Dates are always a string in ISO standard yyyy-mm-dd

    """

    # defining class variables (shared between all objects)

    #initialization method, just passing the name of the muscle
    def __init__(self, name: str):
        self.name = name
        self.tracking = ["0001-01-01"]
        self.work = ["0001-01-01"]
        self.desc = "unset"

    #method for adding a date when the muscle was sore
    def track(self, date, dest = "s") -> None:
        if dest == "s" or dest == "sw":
            if date not in self.tracking:
                self.tracking.append(date)
        if dest == "w" or dest == "sw":
            if date not in self.work:
                self.work.append(date)
        self.tracking.sort()
        self.work.sort()

    def untrack(self, date, dest = "s") -> None:
        if dest == "s" or dest == "sw":
            if date in self.tracking:
                self.tracking.remove(date)
        if dest == "w" or dest == "sw":
            if date in self.work:
                self.work.remove(date)
        self.tracking.sort()
        self.work.sort()

    #method for checking if muscle was sore on a given date, returns a boolean
    def is_sore(self, date) -> bool:
        if date in self.tracking:
            return True
        else:
            return False
    #method for checking if muscle was worked on a given date, returns a boolean
    def is_work(self, date) -> bool:
        if date in self.work:
            return True
        else:
            return False

    def set_desc(self, date = datetime.now().date()):

        if self.is_sore(date.isoformat()):
            self.desc = "i'm still sore"
        elif self.work[-1] > self.tracking[-1]:
            self.desc = "never got sore"
        elif datetime.fromisoformat(self.tracking[-1]) > datetime.now() + timedelta(days=-2):
            self.desc = "healed just on time"
        else:
            self.desc = "healed a while ago"

# Saving to file called data/data.pkl
def save_state(obj):
    try:
        print("Saving...\n")
        pickle.dump(obj, open('data/data.pkl', 'wb'))
        print("State saved!\n")
    except:
        print("Saving error!\n")

# ckeck current muscles against form muscles and add soreness date to tracking
def add_date_to_muscles(request) -> None:

    global current_muscles
    
    today = datetime.now().date().isoformat()

    # Step 1: add checked muscles soreness
    for var in request.form:
        if var[:4] == "sore":
            for muscle in current_muscles:
                if muscle.name == var[5:]:
                    muscle.track(today, "s")
        
        if var[:4] == "work":
            for muscle in current_muscles:
                if muscle.name == var[5:]:
                    muscle.track(today, "w")

    # Step 2: remove unchecked muscles soreness
    for muscle in current_muscles:
        if muscle.is_sore(today):
            if "sore-" + muscle.name not in request.form:
                muscle.untrack(today, "s")

        if muscle.is_work(today):
            if "work-" + muscle.name not in request.form:
                muscle.untrack(today, "w")

# setting description based on date last sore
def set_desc(current_muscles):

    today = datetime.now().date()

    for muscle in current_muscles:
        if muscle.is_sore(today.isoformat()):
            muscle.desc = "i'm still sore"
        elif muscle.work[-1] > muscle.tracking[-1]:
            muscle.desc = "never got sore"
        elif datetime.fromisoformat(muscle.tracking[-1]) > datetime.now() + timedelta(days=-2):
            muscle.desc = "healed just on time"
        else:
            muscle.desc = "healed a while ago"

### STARTING THE APP ###

try:
    loaded = pickle.load(open('data/data.pkl', 'rb'))
except:
    loaded = None

# Load data or setup default muscles for a first start
if loaded:
    print("Loading...\n")
    current_muscles = loaded
    print("State Loaded!\n")
else:
    print("No save file, loading defaults\n")
    for muscle in default_muscles:
        current_muscles.append(Muscle(muscle))

### TEST: ###
#current_muscles[0].track(datetime.now().date().isoformat()) #testing purposes
#current_muscles[4].track(datetime.now().date().isoformat(), "sw") #testing purposes
#current_muscles[3].track((datetime.now().date() + timedelta(days=-2)).isoformat(), "w") #testing purposes
#current_muscles[3].track((datetime.now().date() + timedelta(days=-1)).isoformat(), "s") #testing purposes
###END TEST

### FLASK: RENDERING HTML ###
app = Flask(__name__)

# Index page
@app.route("/")
def index():

    today = datetime.now().date().isoformat()
    yesterday = datetime.now() + timedelta(days = -1)
    yesterday = yesterday.date().isoformat()

    set_desc(current_muscles)

    return render_template("index.html", current_muscles = current_muscles, today = today, yesterday = yesterday)

# Input page handling input for today
@app.route('/input', methods=['POST', 'GET'])
def input():
    error = None
    today = datetime.now().date().isoformat()

    # handle form input to muscle object
    if request.method == 'POST':
        add_date_to_muscles(request)

        save_state(current_muscles)

        return redirect(url_for("index"))

    return render_template('input.html', error=error, current_muscles = current_muscles, today = today)


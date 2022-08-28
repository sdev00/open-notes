from flask import Flask, request, render_template
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def show_notes():
    # get all files in notes folder
    note_files = os.listdir("notes")
    
    # add all notes to list
    notes = []
    for index, note_file in enumerate(note_files):
        note_dict = get_from_file(note_file)
        notes.append(note_dict)
    
    # sort notes by date and time
    notes.sort(key=lambda x: (x['date'], x['time']), reverse=False)

    # map each note to (index, note)
    notes = list(enumerate(notes))[::-1]
    
    # return notes
    return render_template("gallery.html", notes=notes)

@app.route('/new', methods =["GET", "POST"])
def new_note():
    # count how many notes are in the folder
    notes = set(os.listdir("notes"))

    if request.method == "POST":
        # getting input with name = fname in HTML form
        note = request.form.get("new-note")
        author = request.form.get("author")
        
        # get the calendar date
        date = datetime.now().strftime("%Y-%m-%d")

        # get the time
        time = datetime.now().strftime("%H:%M:%S")

        # get the milliseconds
        milliseconds = datetime.now().timestamp() * 1000

        # write note to new file
        write_to_file(author, date, time, milliseconds, note)

        # get the note dictionary
        note_dict = get_from_file(f"note-{date}-{milliseconds}.txt")

        # count how many notes are in the folder
        count = len(os.listdir("notes"))
        
        return render_template("note-submitted.html", note=(count, note_dict))
    return render_template("new-note.html")

def write_to_file(author, date, time, milliseconds, note):
    with open(f'notes/note-{date}-{milliseconds}.txt', 'w') as f:
        f.write(f'{author}\n{date}\n{time}\n{note}')

def get_from_file(file):
    with open(f'notes/{file}', 'r') as f:
        text = f.read().splitlines()
        author = text[0]
        date = text[1]
        time = text[2]
        note = text[3:]
        return {"author": author, "date": date, "time": time, "note": note}
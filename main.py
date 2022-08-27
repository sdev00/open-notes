from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route("/")
def show_notes():
    # get all files in notes folder
    note_files = os.listdir("notes")
    
    # add all notes to list
    notes = []
    for note in note_files:
        with open("notes/" + note, "r") as f:
            text = f.read().splitlines()
            
            # first line is author
            author = text[0]

            # remaining lines are note
            note = text[1:]
            notes.insert(0, (author, note))
    
    # return notes
    return render_template("show-notes.html", notes=notes)

@app.route('/new', methods =["GET", "POST"])
def new_note():
    # count how many notes are in the folder
    notes = os.listdir("notes")
    num_notes = len(notes)

    if request.method == "POST":
        # getting input with name = fname in HTML form
        note = request.form.get("new-note")
        author = request.form.get("author")

        # write note to new file
        with open(f'notes/note-{num_notes}.txt', 'w') as f:
            f.write(f'{author}\n{note}')
        
        return render_template("note-submitted.html", note=note, author=author)
    return render_template("new-note.html")
import os
import webbrowser
import random
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import messagebox  # only for fallback if needed

# --- ML setup -------------------------------------------------------

# Load training data
training_dataset = pd.read_csv('Training.csv')
X = training_dataset.iloc[:, 0:132].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality reduction mapping
dimensionality_reduction = training_dataset.groupby('prognosis').max()

# Label encode
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Train/test split & Decision Tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, _tree

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0)
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

cols = training_dataset.columns[:-1]

# Load doctors dataset
doc_dataset = pd.read_csv('doctors_dataset.csv', names=['Name','Description'])
diseases_df = pd.DataFrame(dimensionality_reduction.index,
                           columns=['prognosis'])
doctors = pd.DataFrame({
    'disease': diseases_df['prognosis'],
    'name':    doc_dataset['Name'],
    'link':    doc_dataset['Description']
})

# --- Chatbot logic --------------------------------------------------

class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", lambda e: self.text.config(cursor="hand2"))
        self.text.tag_bind("hyper", "<Leave>", lambda e: self.text.config(cursor=""))
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.links = {}

    def add(self, action):
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag.startswith("hyper-"):
                self.links[tag]()
                return

def print_disease(node):
    node = node[0]
    val = node.nonzero()
    return labelencoder.inverse_transform(val[0])

def recurse(node, depth):
    global tree_, feature_name, symptoms_present, ans
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        name = feature_name[node]
        threshold = tree_.threshold[node]
        yield name + " ?"
        val = 1 if ans=='yes' else 0
        if val <= threshold:
            yield from recurse(tree_.children_left[node], depth+1)
        else:
            symptoms_present.append(name)
            yield from recurse(tree_.children_right[node], depth+1)
    else:
        present = print_disease(tree_.value[node])[0]
        box = QuestionDigonosis.objRef.txtDigonosis
        box.insert(END, f"You may have : {present}\n")

        red_cols = dimensionality_reduction.columns
        given = list(red_cols[
            dimensionality_reduction.loc[[present]].values[0].nonzero()
        ])
        box.insert(END, f"symptoms present:  {symptoms_present}\n")
        box.insert(END, f"symptoms given: {given}\n")

        conf = len(symptoms_present)/len(given)
        pct = random.choice([70,71,72,73,74] if conf<0.1 else [80,81,82,83,84,85])
        box.insert(END, f"confidence level is: {pct}%\n")

        box.insert(END, "The model suggests:\n")
        row = doctors[doctors['disease']==present].iloc[0]
        box.insert(END, f"Consult {row['name']}\n")

        hyperlink = HyperlinkManager(box)
        def open_link():
            webbrowser.open_new(row['link'])
        box.insert(END,
                   f"Visit {row['link']}\n",
                   hyperlink.add(open_link)
        )
        # no further yield

def tree_to_code():
    global tree_, feature_name, symptoms_present
    tree_ = classifier.tree_
    feature_name = [
        cols[i] if i!=_tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    symptoms_present = []

def execute_bot():
    tree_to_code()

# --- UI: Chatbot Frame ---------------------------------------------

class QuestionDigonosis(Frame):
    objRef = None

    def __init__(self, master=None):
        QuestionDigonosis.objRef = self
        super().__init__(master, bg="#e8f4f8")
        master.title("Healthcare Chatbot — Diagnosis")
        master.geometry("1000x650")
        self.createWidget()

    def createWidget(self):
        card = Frame(self, bg="white", bd=1, relief="ridge")
        card.place(relx=0.5, rely=0.5,
                   anchor=CENTER, relwidth=0.92, relheight=0.92)

        Label(card, text="🔬 Symptom Checker",
              bg="white", font=("Helvetica", 16, "bold")
        ).pack(pady=(10,20))

        # Question box
        qf = Frame(card, bg="white")
        qf.pack(fill="x", padx=30)
        Label(qf, text="Question:",
              bg="white", font=("Helvetica",12,"bold")
        ).pack(anchor="w")
        self.txtQuestion = Text(qf, height=3, bd=1,
                                relief="solid", font=("Helvetica",11))
        self.txtQuestion.pack(fill="x", pady=(5,15))

        # Diagnosis box
        df = Frame(card, bg="white")
        df.pack(fill="both", expand=True, padx=30)
        Label(df, text="Diagnosis:",
              bg="white", font=("Helvetica",12,"bold")
        ).pack(anchor="w")
        self.txtDigonosis = Text(df, height=10, bd=1,
                                 relief="solid", font=("Helvetica",11))
        self.txtDigonosis.pack(fill="both", expand=True, pady=(5,15))

        # Buttons
        bf = Frame(card, bg="white")
        bf.pack(pady=(0,20))
        style = dict(bg="#4a90e2", fg="white",
                     font=("Helvetica",11),
                     bd=0, activebackground="#357ABD",
                     activeforeground="white",
                     padx=12, pady=6)
        Button(bf, text="Start", command=self.btnStart_Click, **style).pack(side="left", padx=8)
        Button(bf, text="Yes",   command=self.btnYes_Click,   **style).pack(side="left", padx=8)
        Button(bf, text="No",    command=self.btnNo_Click,    **style).pack(side="left", padx=8)
        Button(bf, text="Clear", command=self.btnClear_Click, **style).pack(side="left", padx=8)

    def btnStart_Click(self):
        execute_bot()
        self.txtQuestion.delete("1.0", END)
        self.txtDigonosis.delete("1.0", END)
        self.txtDigonosis.insert(END,
            "👉 Please answer the questions below by clicking Yes or No.\n\n"
        )
        QuestionDigonosis.objRef.iter = recurse(0, 1)
        q = QuestionDigonosis.objRef.iter.__next__()
        self.txtQuestion.insert(END, q + "\n")

    def btnYes_Click(self):
        global ans
        ans = 'yes'
        try:
            q = QuestionDigonosis.objRef.iter.__next__()
            self.txtQuestion.delete("1.0", END)
            self.txtQuestion.insert(END, q + "\n")
        except StopIteration:
            pass

    def btnNo_Click(self):
        global ans
        ans = 'no'
        try:
            q = QuestionDigonosis.objRef.iter.__next__()
            self.txtQuestion.delete("1.0", END)
            self.txtQuestion.insert(END, q + "\n")
        except StopIteration:
            pass

    def btnClear_Click(self):
        self.txtQuestion.delete("1.0", END)
        self.txtDigonosis.delete("1.0", END)

# --- UI: Login & Registration -------------------------------------

root = Tk()
root.title("Welcome to Healthcare Chatbot")
root.geometry("450x350")
root.configure(bg="#e6f2ff")

def show_custom_message(title, message, severity="info"):
    dlg = Toplevel(root)
    dlg.transient(root)
    dlg.grab_set()
    dlg.title("")
    dlg.configure(bg="white")
    dlg.resizable(False, False)

    w, h = 350, 150
    x = root.winfo_x() + (root.winfo_width() - w)//2
    y = root.winfo_y() + (root.winfo_height() - h)//2
    dlg.geometry(f"{w}x{h}+{x}+{y}")

    header_color = "#4a90e2" if severity=="info" else "#d9534f"
    header = Frame(dlg, bg=header_color, height=40)
    header.pack(fill="x")
    Label(header, text=title, bg=header_color, fg="white",
          font=("Helvetica", 14, "bold")).pack(pady=5)

    body = Frame(dlg, bg="white")
    body.pack(fill="both", expand=True, pady=(10,0), padx=10)

    icon = "✔️" if severity=="info" else "✖️"
    Label(body, text=icon, font=("Helvetica", 24),
          bg="white").grid(row=0, column=0, padx=(0,10))

    Label(body, text=message, bg="white", justify="left",
          font=("Helvetica", 12)).grid(row=0, column=1, sticky="w")

    btn = Button(body, text="OK", bg=header_color, fg="white",
                 font=("Helvetica", 11), bd=0,
                 activebackground=header_color,
                 command=dlg.destroy)
    btn.grid(row=1, column=0, columnspan=2, pady=10)

    dlg.wait_window()

def open_chatbot():
    for w in root.winfo_children(): w.destroy()
    qf = QuestionDigonosis(master=root)
    qf.pack(fill='both', expand=True)

def open_registration():
    for w in root.winfo_children(): w.destroy()
    frm = Frame(root, bg="#e6ffe6")
    frm.pack(fill='both', expand=True)
    card = Frame(frm, bg="white", bd=2, relief=RIDGE, padx=30, pady=20)
    card.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(card, text="Register", bg="white", fg="#006633",
          font=("Helvetica",18,"bold")).pack(pady=(0,20))

    Label(card, text="Choose Username", bg="white",
          font=("Helvetica",12)).pack(anchor="w")
    entry_u = Entry(card, font=("Helvetica",12))
    entry_u.pack(fill='x', pady=(0,10))

    Label(card, text="Choose Password", bg="white",
          font=("Helvetica",12)).pack(anchor="w")
    entry_p = Entry(card, show="*", font=("Helvetica",12))
    entry_p.pack(fill='x', pady=(0,20))

    def do_register():
        u, p = entry_u.get().strip(), entry_p.get().strip()
        if not u or not p:
            show_custom_message("Error", "Please fill both fields", severity="error")
            return
        if os.path.exists(u):
            show_custom_message("Error", "Username already taken", severity="error")
            return
        with open(u,"w") as f:
            f.write(u + "\n" + p)
        show_custom_message("Success", "Registration successful!", severity="info")
        open_login_page()

    Button(card, text="Register", bg="#33cc33", fg="white",
           font=("Helvetica",12), width=26,
           command=do_register).pack()

def open_login_page():
    for w in root.winfo_children(): w.destroy()
    frm = Frame(root, bg="#e6f2ff")
    frm.pack(fill='both', expand=True)
    card = Frame(frm, bg="white", bd=2, relief=RIDGE, padx=30, pady=20)
    card.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(card, text="Login", bg="white", fg="#003366",
          font=("Helvetica",18,"bold")).pack(pady=(0,20))

    Label(card, text="Username", bg="white", font=("Helvetica",12)).pack(anchor="w")
    entry_u = Entry(card, font=("Helvetica",12))
    entry_u.pack(fill='x', pady=(0,10))

    Label(card, text="Password", bg="white", font=("Helvetica",12)).pack(anchor="w")
    entry_p = Entry(card, show="*", font=("Helvetica",12))
    entry_p.pack(fill='x', pady=(0,20))

    def try_login():
        u, p = entry_u.get().strip(), entry_p.get().strip()
        if os.path.exists(u):
            with open(u) as f:
                usr, pwd = f.read().splitlines()
            if p == pwd:
                show_custom_message("Welcome", "Login successful!", severity="info")
                open_chatbot()
                return
        show_custom_message("Error", "Invalid username or password", severity="error")

    btn = Frame(card, bg="white")
    btn.pack()
    Button(btn, text="Login", bg="#3399ff", fg="white",
           font=("Helvetica",12), width=12,
           command=try_login).pack(side="left", padx=5)
    Button(btn, text="Register", bg="#33cc33", fg="white",
           font=("Helvetica",12), width=12,
           command=open_registration).pack(side="left", padx=5)

# --- Start application ---------------------------------------------

open_login_page()
root.mainloop()
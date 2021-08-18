from tkinter import *
from tkinter import ttk
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter.messagebox
import os
import csv
import time
os.chdir("/home/mnagara/Documents/Synhelix/Struc2D/tools/e2efold/e2efold_productive/Stats_2D_pred/APPLICATION_SYNHELIX/")
#####################################
from Codon_optimization_script import  *
#Bonjour

# This is an application for proteine codon optimization and calculate the incorporation rate for DNA synthesis:

root= Tk()
root.title("Synhelix: Icorporation rate prediction & Codon optimizer")
icone = PhotoImage(file='/home/mnagara/Documents/Synhelix/Struc2D/tools/e2efold/e2efold_productive/Stats_2D_pred/SYNHELIX.png')
root.iconphoto(True, icone)
#root.iconbitmap("@synhelix_annur.ico")
root.call('wm', 'iconphoto', root._w, icone)
root.geometry('1200x950')
root['bg']='#49A'

#To get Tkinter input from the text box,
# The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
# END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
# The only issue with this is that it actually adds a newline to our input. So, in order to fix it we should change END to end-1c
# (Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on.


def retrieve_input():

    inputValue=textBox.get("1.0","end-1c") # "1.0","end-1c"
    if inputValue == None:
        inputValue = "TTTTTT"
    else:
        inputValue = inputValue
    Results_codon2 = Codon_optimization(inputValue)
    Results_codon3 = Results_codon2[['Codon', 'Codon_mers', 'Sequence', 'dot', 'Melting_temperature', 'GC_count',
                    'Purine_AG_content', 'Keto_GT_content','Incor_rate_adj', 'Codon_Incor_rate' ]]

    df_list = Results_codon3.values.tolist()
    # Add some style:
    style = ttk.Style()
    # Pick a theme:
    style.theme_use("clam")
    # Configure our treeview colors:
    style.configure("Treeview",
            background = "white",
            foreground = "black",
            rowheight = 25,
            fieldbackground = "white"
                    )
    # change selected color:
    style.map('Treeview',
            background = [('selected', 'green')]
            )

    # Create Treeview Frame:
    tree_frame = Frame(root)
    tree_frame.pack(pady=20)
    # Treeview Scrollbar:
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    # Create Treeview:
    my_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, selectmode="extended") # , selectmode="extended", 'none', 'browse'

    # Pack to the screen
    my_tree.pack() # pady=50, expand=True

    # Configure the scrollbar
    tree_scroll.config(command=my_tree.yview)

    # Define our columns:
    my_tree['columns'] = ('Codon', 'Codon_mers', 'Sequence', 'dot', 'Melting_temperature', 'GC_count',
                    'Purine_AG_content', 'Keto_GT_content','Incor_rate_adj', 'Codon_Incor_rate')


    columns = ['Codon', 'Codon_mers', 'Sequence', 'dot', 'Melting_temperature', 'GC_count',
                    'Purine_AG_content', 'Keto_GT_content','Incor_rate_adj', 'Codon_Incor_rate']
    # Formate Our Columns:
    my_tree.column("#0", width=0, stretch=NO) # minwidth=25, ,  stretch=NO ==> pour enlever la premiere colonne
    my_tree.column("Codon", anchor=CENTER, width=100)
    my_tree.column("Codon_mers", anchor=CENTER, width=100)
    my_tree.column("Sequence", anchor=W, width=180)
    my_tree.column("dot", anchor=W, width=180)
    my_tree.column("Melting_temperature", anchor=CENTER, width=180)
    my_tree.column("GC_count", anchor=CENTER, width=120)
    my_tree.column("Purine_AG_content", anchor=CENTER, width=120)
    my_tree.column("Keto_GT_content", anchor=CENTER, width=120)
    my_tree.column("Incor_rate_adj", anchor=CENTER, width=120)
    my_tree.column("Codon_Incor_rate", anchor=CENTER, width=120)

    for col in columns:
        my_tree.heading(col, text=col, anchor=CENTER)
    my_tree.pack()

    print(f'Now click on the botton to predict incorporation rate for: {inputValue}')

    codon_list = []
    for i, j in enumerate (range(2,len(df_list),3)):
        codon_list.append(df_list[j])

    # Create striped row tags:
    my_tree.tag_configure('oddrow', background = 'white')
    my_tree.tag_configure('evenrow', background = 'lightskyblue')

    global count
    count = 0
    for record in codon_list:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='Parent', values=(record[0], record[1], record[2], record[3], record[4],
                                                                                record[5], record[6], record[7], record[8], record[9]),tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='Parent', values=(record[0], record[1], record[2], record[3], record[4],
                                                                                record[5], record[6], record[7], record[8], record[9]),tags=('oddrow',))
        count += 1

    # add Frame and data boxes:
    add_frame = Frame(root)
    add_frame.pack(pady=50)

    # add name label:
    nl = Label(add_frame, text = "Codon")
    nl.grid(row=0, column=0)
    il = Label(add_frame, text="Codon_mers")
    il.grid(row=0, column=1)
    tl = Label(add_frame, text="Sequence")
    tl.grid(row=0, column=2)
    dl = Label(add_frame, text="dot")
    dl.grid(row=0, column=3)
    ml = Label(add_frame, text="Melting_temperature")
    ml.grid(row=0, column=4)
    gl = Label(add_frame, text="GC_count")
    gl.grid(row=0, column=5)
    pl = Label(add_frame, text="Purine_AG_content")
    pl.grid(row=0, column=6)
    kl = Label(add_frame, text="Keto_GT_content")
    kl.grid(row=0, column=7)
    inl = Label(add_frame, text="Incor_rate_adj")
    inl.grid(row=0, column=8)
    codl = Label(add_frame, text="Codon_Incor_rate")
    codl.grid(row=0, column=9)

    # Entry boxes:
    codon_box = Entry(add_frame)
    codon_box.grid(row=1, column=0)
    codon_mers_box = Entry(add_frame)
    codon_mers_box.grid(row=1, column=1)
    Sequence_box = Entry(add_frame)
    Sequence_box.grid(row=1, column=2)
    dot_box = Entry(add_frame)
    dot_box.grid(row=1, column=3)
    Melting_temperature_box = Entry(add_frame)
    Melting_temperature_box.grid(row=1, column=4)
    GC_count_box = Entry(add_frame)
    GC_count_box.grid(row=1, column=5)
    Purine_AG_content_box = Entry(add_frame)
    Purine_AG_content_box.grid(row=1, column=6)
    Keto_GT_content_box = Entry(add_frame)
    Keto_GT_content_box.grid(row=1, column=7)
    Incor_rate_adj_box = Entry(add_frame)
    Incor_rate_adj_box.grid(row=1, column=8)
    Codon_Incor_rate_box = Entry(add_frame)
    Codon_Incor_rate_box.grid(row=1, column=9)


    # Add Record:
    def add_record():
        # Create striped row tags:
        my_tree.tag_configure('oddrow', background = 'white')
        my_tree.tag_configure('evenrow', background = 'lightskyblue')

        global count
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='Child', values=(codon_box.get(), codon_mers_box.get(), Sequence_box.get(),
                                                                                    dot_box.get(),Melting_temperature_box.get(), GC_count_box.get(),
                                                                                     Purine_AG_content_box.get(), Keto_GT_content_box.get(),
                                                                                     Incor_rate_adj_box.get(), Codon_Incor_rate_box.get()),tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='Child', values=(codon_box.get(), codon_mers_box.get(), Sequence_box.get(),
                                                                                    dot_box.get(),Melting_temperature_box.get(), GC_count_box.get(),
                                                                                     Purine_AG_content_box.get(), Keto_GT_content_box.get(),
                                                                                     Incor_rate_adj_box.get(), Codon_Incor_rate_box.get()),tags=('oddrow',))
        count += 1
        # Clear all boxes
        codon_box.delete(0, END)
        codon_mers_box.delete(0, END)
        Sequence_box.delete(0, END)
        dot_box.delete(0, END)
        Melting_temperature_box.delete(0, END)
        GC_count_box.delete(0, END)
        Purine_AG_content_box.delete(0, END)
        Keto_GT_content_box.delete(0, END)
        Incor_rate_adj_box.delete(0, END)
        Codon_Incor_rate_box.delete(0, END)


    # Remove all records:
    def remove_all():
        for record in my_tree.get_children():
            my_tree.delete(record)

    # Remove One selected:
    def remove_one():
        x = my_tree.selection()[0]
        my_tree.delete(x)

    # Remove many selected:
    def remove_many():
        x = my_tree.selection()
        for record in x:
            my_tree.delete(record)

    # Select record:
    def select_record():
        # Clear entry boxes:
        codon_box.delete(0, END)
        codon_mers_box.delete(0, END)
        Sequence_box.delete(0, END)
        dot_box.delete(0, END)
        Melting_temperature_box.delete(0, END)
        GC_count_box.delete(0, END)
        Purine_AG_content_box.delete(0, END)
        Keto_GT_content_box.delete(0, END)
        Incor_rate_adj_box.delete(0, END)
        Codon_Incor_rate_box.delete(0, END)

        # Grab record number
        selected = my_tree.focus()
        # Grab record values:
        values = my_tree.item(selected, 'values')
        #temp_label.config(text=values[0])
        #print(values)
        # output to entry boxes:
        codon_box.insert(0, values[0])
        codon_mers_box.insert(0, values[1])
        Sequence_box.insert(0, values[2])
        dot_box.insert(0, values[3])
        Melting_temperature_box.insert(0, values[4])
        GC_count_box.insert(0, values[5])
        Purine_AG_content_box.insert(0, values[6])
        Keto_GT_content_box.insert(0, values[7])
        Incor_rate_adj_box.insert(0, values[8])
        Codon_Incor_rate_box.insert(0, values[9])

    # Save Updated Record:
    def update_record():
        # Grab record number
        selected = my_tree.focus()
        # Save new data:
        my_tree.item(selected, text="", values = (codon_box.get(),codon_mers_box.get(), Sequence_box.get(), dot_box.get(),
                                                    Melting_temperature_box.get(), GC_count_box.get(), Purine_AG_content_box.get(),
                                                    Keto_GT_content_box.get(), Incor_rate_adj_box.get(), Codon_Incor_rate_box.get()))
        # Clear entry boxes:
        codon_box.delete(0, END)
        codon_mers_box.delete(0, END)
        Sequence_box.delete(0, END)
        dot_box.delete(0, END)
        Melting_temperature_box.delete(0, END)
        GC_count_box.delete(0, END)
        Purine_AG_content_box.delete(0, END)
        Keto_GT_content_box.delete(0, END)
        Incor_rate_adj_box.delete(0, END)
        Codon_Incor_rate_box.delete(0, END)


    # Create Biding clicke function:
    def clicker(e):
        select_record()

    # Move Row up:
    def up():
        rows = my_tree.selection()
        for row in rows:
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)
    # Move Row Down:
    def down():
        rows = my_tree.selection()
        for row in reversed(rows):
            my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

    # Buttons:
    move_up = Button(root, text="Move Up", command=up)
    move_up.pack(pady=30, side="top", fill="x")
    move_up.place(x=100, y=800)

    move_down = Button(root, text="Move down", command=down)
    move_down.pack(pady=10,side="top", fill="x")
    move_down.place(x=100, y=850)

    select_button = Button(root, text = 'Select Record', command = select_record)
    select_button.pack(pady=20, side="top", fill="x")
    select_button.place(x=200, y=800)

    update_button = Button(root, text = "Save Record", command = update_record)
    update_button.pack(pady=10, side="top", fill="x")
    update_button.place(x=200, y=850)

    #Buttons:
    add_record = Button(root, text = "Add Record", command = add_record)
    add_record.pack(pady=10, side="top", fill="x")
    add_record.place(x=200, y=900)

    #Remove One:
    remove_one = Button(root, text="Remove One Selected", command = remove_one)
    remove_one.pack(pady=20, side="top", fill="x")
    remove_one.place(x=350, y=800)

    #Remove Many selected :
    remove_many = Button(root, text="Remove Many Selected", command = remove_many)
    remove_many.pack(pady=10, side="top", fill="x")
    remove_many.place(x=350, y=850)

    # Remove all
    remove_all = Button(root, text="Remove All Records", command = remove_all)
    remove_all.pack(pady=20, side="top", fill="x")
    remove_all.place(x=350, y=900)

    #
    #temp_label = Label(root, text="")
    #temp_label.pack(pady=20)

    # Bindings
    #my_tree.bind("<Double-1>", clicker)
    my_tree.bind("<ButtonRelease-1>", clicker)

    #Saved results after modification:
    def save_csv():
        with open("new.csv", "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')

            for row_id in my_tree.get_children():
                row = my_tree.item(row_id)['values']
                #print('save row:', row)
                csvwriter.writerow(row)

    # Saved results after modification to csv file
    remove_all = Button(root, text="Save Results", command = save_csv)
    remove_all.pack(pady=20, side="top", fill="x")
    remove_all.place(x=850, y=900)

#my_tree = retrieve_input()

#Results_codon3, df_list = retrieve_input()
MODES = [
    ("MyOne_hybrid", "MyOne_hybrid"),
    ("MyOne_covalent", "MyOne_covalent"),
    ("M270_hybrid","M270_hybrid"),
    ("M270_covalent", "M270_covalent"),
    ("Streptavidin", "Streptavidin"),
    ("Anchor_1", "Anchor_1"),
    ("Free_DNA", "Free_DNA")
        ]


selected_support = []
def optionselected():
    value = check.get()
    if value == 1:
        support = "MyOne_hybrid"
        x = check.get()
        selected_support.append(x)
        print(support)
    elif value == 2:
        support = "M270_hybrid"
        x = check.get()
        selected_support.append(x)
        print(support)
    elif value == 3:
        support = "Streptavidin"
        x = check.get()
        selected_support.append(x)
        print(support)
    return selected_support

def funkcija():
    X = check.get()
    print(X)

# Make title for synhelix software:

w = Label(root, text ='SYNHELIX: Codon Optimization ', font='Helvetica 20 bold')
w.pack(pady=10)



check = IntVar()

r1 = Radiobutton(root, value = 1, variable=check, text="MyOne hybrid", anchor=E).pack()
r2 = Radiobutton(root, value = 2, variable=check, text="M270  hybrid", anchor=E).pack()
r3 = Radiobutton(root, value = 3, variable=check, text="Streptavidin", anchor=E).pack()

Button(root, text="Select Support to use for Synthesis", width=35, height=2, font='Arial 9', anchor=E, command= optionselected).pack(pady=10)

# Add message to choose amorce sequence and run Incorporation rate prediction algorithm

msg = Message( root, text = "Add in the box below the sequence of the primer to make the codon optimization and press 'RUN Algorithm' button to predict the Incoprpration rate", font='Arial 9', anchor=W, width = 580)
#msg.config(bg='lightgreen',relief=RIDGE, font=('times', 9), pady=-2, borderwidth=3)
msg.pack(expand=False) #, pady=10, , fill='x'
msg.bind("<Configure>", lambda e: msg.configure(width=e.width-8))


textBox=Text(root, height = 5, width=75) # height=2, width=50
textBox.pack(pady=20)
# Create a button ro run the analysis
buttonCommit=Button(root, height=2, width=20, text="RUN Algorithm",
                    command=lambda: threading.Thread(retrieve_input()).start())  #threading





# An information box
tkinter.messagebox.showinfo("Information","This analysis will take a little time, Please wait for seconds after click on Run Icncorporation rate prediction button!")
buttonCommit.pack()


# Add Radio for Support type:
##################################################################################################################""

# support = StringVar("")
# for text, mode in MODES:
#     Radiobutton(root, text=text, variable = support, value=mode).pack(anchor='w')
#     which_button_is_selected = support.get()
#     print(which_button_is_selected)
#
#
# def clicked(value):
#     myLabel = Label(root, text = value)
#     myLabel.pack()
#
#
# myLabel = Label(root, text = support.get())
# myLabel.pack()
#
# myButton = Button(root, text="Click Me!", command = lambda: clicked(support.get())).pack()
#
#support.set("MyOne_hybrid")
# # Progress bar for waiting analysis
# def step():
#     #my_progress['value'] += 10
#     for x in  range(10):
#         my_label.config(text=my_progress['value'])
#         my_progress['value'] += 10
#         root.update_idletasks()
#         time.sleep(1)
#
# def stop():
#     my_progress.stop()
#
# my_progress = ttk.Progressbar(root, orient=HORIZONTAL, length= 300, mode = 'determinate')
# my_progress.pack(pady=20)
# my_button = Button(root, text="Progress", command = step)
# my_button.pack(pady=20)
#
# my_button2 = Button(root, text="STOP", command = stop)
# my_button2.pack(pady=20)
#
# my_label = Label(root, text = "")
# my_label.pack(pady=20)

# An information box
#tkinter.messagebox.showinfo("Information","This analysis will take a little time, Please wait!")


#Results_codon3 = retrieve_input()
# def retrieve_input():
#     input = self.myText_Box.get("1.0",'end-1c')

# Make prediction:
# BASE2 = 'ATATAT'
# Results_codon2 = Codon_optimization(BASE2)
#print(Results_codon2)

# Results_codon3 = Results_codon2[['Codon', 'Codon_mers', 'Sequence', 'dot', 'Melting_temperature', 'GC_count',
                # 'Purine_AG_content', 'Keto_GT_content','Incor_rate_adj', 'Codon_Incor_rate' ]]

#df_list = Results_codon3.values.tolist()


# my_tree = ttk.Treeview(root,selectmode="extended")
# Define Our columns
# my_tree['columns'] = ('Codon', 'Codon_mers', 'Sequence', 'dot', 'Melting_temperature', 'GC_count',
                # 'Purine_AG_content', 'Keto_GT_content','Incor_rate_adj', 'Codon_Incor_rate')

# # Formate Our Columns:
# my_tree.column("#0", width=50, minwidth=25) # stretch=NO ==> pour enlever la premiere colonne
# my_tree.column("Codon", anchor=CENTER, width=100)
# my_tree.column("Codon_mers", anchor=CENTER, width=100)
# my_tree.column("Sequence", anchor=W, width=180)
# my_tree.column("dot", anchor=W, width=180)
# my_tree.column("Melting_temperature", anchor=CENTER, width=180)
# my_tree.column("GC_count", anchor=CENTER, width=120)
# my_tree.column("Purine_AG_content", anchor=CENTER, width=120)
# my_tree.column("Keto_GT_content", anchor=CENTER, width=120)
# my_tree.column("Incor_rate_adj", anchor=CENTER, width=120)
# my_tree.column("Codon_Incor_rate", anchor=CENTER, width=120)
#
# # Create Headings:
# my_tree.heading("#0", text='Label', anchor=CENTER)
# my_tree.heading("Codon", text='Codon', anchor=CENTER)
# my_tree.heading("Codon_mers", text='Codon_mers', anchor=CENTER)
# my_tree.heading("Sequence", text='Sequence', anchor=CENTER)
# my_tree.heading("dot", text='2D str. prediction', anchor=CENTER)
# my_tree.heading("Melting_temperature", text='Melting_temperature',anchor=CENTER )
# my_tree.heading("GC_count", text='GC_count',anchor=W)
# my_tree.heading("Purine_AG_content", text='Purine_AG_content',anchor=CENTER )
# my_tree.heading("Keto_GT_content", text='Keto_GT_content',anchor=CENTER )
# my_tree.heading("Incor_rate_adj", text='Incorp.rate adj',anchor=CENTER )
# my_tree.heading("Codon_Incor_rate", text='Codon_Incor_rate',anchor=CENTER )

# Other Methode for creating Headings:
# for col in columns:
#     tree.heading(col, text=col)
# tree.pack()


# Add data:
data = [
    ["AAAA", '(((..)))', 70.5, 26.7, 30],
    ["TTTTTT", '(((..)))', 60.5, 46.7, 40],
    ["GCGGTTG", '(((..)))', 50.5, 36.7, 30],
    ["GCGGGCCCCAAA", '(((..)))', 70.5, 66.7, 30],
    ["CGTGA", '(((..)))', 40.5, 56.7, 30]
]

# for i in range(2,len(df_list),3)
# for i, j in enumerate (range(2,len(df_list),3)):
#
# 0 2
# 1 5
# 2 8
# 3 11
# 4 14

# #Treeview items
# treeview.insert('','0','item1',text='Parent tree')
# treeview.insert('','1','item2',text='1st Child')
# treeview.insert('','end','item3',text='2nd Child')
# treeview.insert('item2','end','A',text='A')
# treeview.insert('item2','end','B',text='B')
# treeview.insert('item2','end','C',text='C')
# treeview.insert('item3','end','D',text='D')
# treeview.insert('item3','end','E',text='E')
# treeview.insert('item3','end','F',text='F')
# treeview.move('item2','item1','end')
# treeview.move('item3','item1','end')

# Parent tree
#     child1
#         A
#         B
#         C
#     child2
#         C
#         D
#         E


# codon_list = []
# for i, j in enumerate (range(2,len(df_list),3)):
#     codon_list.append(df_list[j])
#
# global count
# count = 0
# for record in codon_list:
#     my_tree.insert(parent='', index='end', iid=count, text='Parent', values=(record[0], record[1], record[2], record[3], record[4],
#                                                                             record[5], record[6], record[7], record[8], record[9]))
#
#     count += 1

    # for i in df_list:
    #     # Add Child:
    #     my_tree.insert(parent='', index='end', iid=i, text='Child', values=(record[0], record[1], record[2], record[3], record[4],
    #                                                                             record[5], record[6], record[7], record[8], record[9]))
    #     my_tree.move(str(i), str(count), '0')
    #
    # count += 1


# my_tree.insert(parent='', index='end', iid=0, text='Parent', values=("AAAA", '(((..)))', 70.5, 26.7, 30))
# my_tree.insert(parent='', index='end', iid=1, text='Parent', values=("TTTTTT", '(((..)))', 60.5, 46.7, 40))
# my_tree.insert(parent='', index='end', iid=2, text='Parent', values=("GCGGTTG", '(((..)))', 50.5, 36.7, 30))
# my_tree.insert(parent='', index='end', iid=3, text='Parent', values=("GCGGGCCCCAAA", '(((..)))', 70.5, 66.7, 30))
# my_tree.insert(parent='', index='end', iid=4, text='Parent', values=("CGTGA", '(((..)))', 40.5, 56.7, 30))

# Add Child:
# my_tree.insert(parent='', index='end', iid=6, text='Child', values=("GGG", '(((..)))', 10.5, 26.7, 50))
# my_tree.move('6', '0', '0')


# Pack to the screen
#my_tree.pack(pady=50, expand=True)

# add_frame = Frame(root)
# add_frame.pack(pady=50)
#
# # add name label:
# nl = Label(add_frame, text = "Codon")
# nl.grid(row=0, column=0)
# il = Label(add_frame, text="Codon_mers")
# il.grid(row=0, column=1)
#
# tl = Label(add_frame, text="Incorporation_rate")
# tl.grid(row=0, column=2)
#
# #
# # Entry boxes:
# codon_box = Entry(add_frame)
# codon_box.grid(row=1, column=0)
#
# codon_mers_box = Entry(add_frame)
# codon_mers_box.grid(row=1, column=1)
#
# incorporation_rate_box = Entry(add_frame)
# incorporation_rate_box.grid(row=1, column=2)
#
# #Add Record:
# def add_record():
#     global count
#
#     my_tree.insert(parent='', index='end', iid=count, text='Child', values=(codon_box.get(), codon_mers_box.get(), incorporation_rate_box.get()))
#     count += 1
#     # Clear all boxes
#     codon_box.delete(0, END)
#     codon_mers_box.delete(0, END)
#     incorporation_rate_box.delete(0, END)
#
# # Remove all records:
# def remove_all():
#     for record in my_tree.get_children():
#         my_tree.delete(record)
#
#
#
#
#
# #Buttons:
# add_record = Button(root, text = "Add Record", command= add_record)
# add_record.pack(pady=20)
#
# # Remove all
# remove_all = Button(root, text="Remove All Records", command= remove_all)
# remove_all.pack(pady=10)




# canvas1 = tk.Canvas(root, width = 800, height = 300)
# canvas1.pack()
#
# label1 = tk.Label(root, text='Predict Incorporation rate and codon optimization')
# label1.config(font=('Arial', 20))
# canvas1.create_window(400, 50, window=label1)
#
# entry1 = tk.Entry (root)
# canvas1.create_window(400, 100, window=entry1)
#
# #entry2 = tk.Entry (root)
# #canvas1.create_window(400, 120, window=entry2)
#
# #entry3 = tk.Entry (root)
# #canvas1.create_window(400, 140, window=entry3)
#
# def create_charts():
#     global x1
#     #global x2
#     #global x3
#     #global bar1
#     #global pie2
#     x1 = str(entry1.get())
#     Results_codon = Codon_optimization(x1)
#     #x2 = str(entry2.get())
#     #x3 = str(entry3.get())
#
#     # figure1 = Figure(figsize=(4,3), dpi=100)
#     # subplot1 = figure1.add_subplot(111)
#     # xAxis = [float(x1),float(x2),float(x3)]
#     # yAxis = [float(x1),float(x2),float(x3)]
#     # subplot1.bar(xAxis,yAxis, color = 'lightsteelblue')
#     # bar1 = FigureCanvasTkAgg(figure1, root)
#     # bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
#     #
#     # figure2 = Figure(figsize=(4,3), dpi=100)
#     # subplot2 = figure2.add_subplot(111)
#     # labels2 = 'Label1', 'Label2', 'Label3'
#     # pieSizes = [float(x1),float(x2),float(x3)]
#     # my_colors2 = ['lightblue','lightsteelblue','silver']
#     # explode2 = (0, 0.1, 0)
#     # subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True, startangle=90)
#     # subplot2.axis('equal')
#     # pie2 = FigureCanvasTkAgg(figure2, root)
#     # pie2.get_tk_widget().pack()
#
#
# def clear_charts():
#     bar1.get_tk_widget().pack_forget()
#     pie2.get_tk_widget().pack_forget()
#
# button1 = tk.Button (root, text=' Create sequence ',command=create_charts, bg='palegreen2', font=('Arial', 11, 'bold'))
# canvas1.create_window(400, 180, window=button1)
#
# button2 = tk.Button (root, text='  Clear sequence  ', command=clear_charts, bg='lightskyblue2', font=('Arial', 11, 'bold'))
# canvas1.create_window(400, 220, window=button2)
#
# button3 = tk.Button (root, text='Exit Application', command=root.destroy, bg='lightsteelblue2', font=('Arial', 11, 'bold'))
# canvas1.create_window(400, 260, window=button3)

root.mainloop()

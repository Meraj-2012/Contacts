from customtkinter import *
from CTkMessagebox import *
from sqlite3 import *


connection = connect("Meraj.db")
cursor = connection.cursor()
command = """
create table if not exists contacts(
id integer primary key autoincrement, 
name text not null, 
call_num text not null
)
"""
cursor.execute(command)
#=======================================================================================================================
def refresh_list(keyword=""):
    for widget in scroll.winfo_children():
        widget.destroy()
    if keyword:
        cursor.execute("select id, name, call_num from contacts where name like ? or call_num like ?", (f"%{keyword}%", f"%{keyword}%"))
    else:
        cursor.execute("select id, name, call_num from contacts")
    for id_, name, phone in cursor.fetchall():
        label = CTkLabel(scroll, text=f"{id_}-{name}      {phone}", fg_color="#202bfe", width=400, height=40, corner_radius=5)
        label.pack(pady=1.5)
#=======================================================================================================================
def search_contacts(event=None):
    keyword = search_box.get().strip()
    refresh_list(keyword)

#=======================================================================================================================
def add_contacts():
    root.withdraw()
    add_window = CTkToplevel(root)
    add_window.title("Add contact")
    add_window.geometry("450x450")
    add_window.resizable(False, False)

    def save():
        full_name = f_name.get().strip() + " " + l_name.get().strip()
        call = call_num.get().strip()
        if not f_name.get().strip() or not l_name.get().strip() or not call:
            CTkMessagebox(title="Error", message="please complete the items!!",width=300, height=150, icon="warning")
            l_name.delete(0, END)
            f_name.delete(0, END)
            call_num.delete(0, END)
        else:
            msg = CTkMessagebox(title="Save", message="Are you sure you want to save?", option_1="Yes", option_2="No", width=300, height=150)
            if msg.get() == "Yes":
                cursor.execute("insert into contacts (name, call_num) values (?, ?)", (full_name, call))
                connection.commit()

                l_name.delete(0, END)
                f_name.delete(0, END)
                call_num.delete(0, END)
                refresh_list()


    def out():
        msg = CTkMessagebox(title="Warning", message="Are you sure you want to Exit?", option_1="Yes", option_2="No", width=300, height=150)
        if msg.get() == "Yes":
            add_window.destroy()
            root.deiconify()

    label_ = CTkLabel(add_window, text="Add contacts", font=("Comic Sans MS", 30, "bold"), corner_radius=20, fg_color="#202bfe", padx=10, pady=10)
    label_.pack(pady=(20, 10))
    frame_entry = CTkFrame(add_window)
    f_name = CTkEntry(frame_entry, placeholder_text="First name", font=("Comic Sans MS", 20, "bold"), corner_radius=5, width=300)
    f_name.pack(pady=(20, 5), padx=20)

    l_name = CTkEntry(frame_entry, placeholder_text="Last name", font=("Comic Sans MS", 20, "bold"), corner_radius=5, width=300)
    l_name.pack()

    call_num = CTkEntry(frame_entry, placeholder_text="Phone", font=("Comic Sans MS", 20, "bold"), corner_radius=5, width=300)
    call_num.pack(pady=20)

    frame_entry.pack(pady=20)
    frame_btn = CTkFrame(add_window, fg_color="#242424")
    btn_cancel = CTkButton(frame_btn, text="Cancel", font=("Comic Sans MS", 20, "bold"), corner_radius=20, width=100, fg_color="#202bfe", command=out)
    btn_cancel.grid(pady=(0, 20), row=0, column=0, padx=(0, 3))

    btn_save = CTkButton(frame_btn, text="Save", font=("Comic Sans MS", 20, "bold"), corner_radius=20, width=100, fg_color="#202bfe", command=save)
    btn_save.grid(pady=(0, 20), row=0, column=1, padx=(3, 0))
    frame_btn.pack()

#=======================================================================================================================
def edit_contacts():
    root.withdraw()
    edit_window = CTkToplevel(root)
    edit_window.title("Edit contacts")
    edit_window.geometry("750x450")
    edit_window.resizable(False, False)

    def edit():
        full_name = f_name_replace.get().strip() + " " + l_name_replace.get().strip()
        call = call_num_replace.get().strip()
        full_id = id_change.get().strip()
        if not full_name or not call or not full_id:
            CTkMessagebox(title="Error", message="please complete the items!!", width=300, height=150, icon="warning")
            id_change.delete(0, END)
            f_name_replace.delete(0, END)
            l_name_replace.delete(0, END)
            call_num_replace.delete(0, END)
        else:
            try:
                msg = CTkMessagebox(title="Edit", message="Are you sure you want to Edit?", option_1="Yes", option_2="No", width=300, height=150)
                if msg.get() == "Yes":

                    cursor.execute("update contacts set name = ?, call_num = ? where id = ?", (full_name, call, int(full_id)))
                    connection.commit()
                    refresh_list()

                    id_change.delete(0, END)
                    f_name_replace.delete(0, END)
                    l_name_replace.delete(0, END)
                    call_num_replace.delete(0, END)
            except:
                CTkMessagebox(title="Error", message="The ID not in contacts!", width=300, height=150, icon="warning")
                id_change.delete(0, END)
                f_name_replace.delete(0, END)
                l_name_replace.delete(0, END)
                call_num_replace.delete(0, END)


    def out():
        msg = CTkMessagebox(title="Warning", message="Are you sure you want to Exit?", option_1="Yes", option_2="No", width=300, height=150)
        if msg.get() == "Yes":
            edit_window.destroy()
            root.deiconify()


    frame = CTkFrame(edit_window, fg_color="#242424")

    label_ = CTkLabel(frame, text="Edit contacts", font=("Comic Sans MS", 30, "bold"), corner_radius=20, fg_color="#202bfe", padx=10, pady=10)
    label_.grid(columnspan=2, pady=20)

    frame_left = CTkFrame(frame)
    label_change = CTkLabel(frame_left, text="Change what?", font=("Comic Sans MS", 20, "bold"), fg_color="#202bfe", padx=5, pady=5, corner_radius=20)
    label_change.pack(pady=(10, 0))

    id_change = CTkEntry(frame_left, placeholder_text="ID", font=("Comic Sans MS", 20, "bold"), corner_radius=5, width=250)
    id_change.pack(pady=20, padx=20)
    frame_left.grid(row=1, column=0, padx=(0, 25))

    frame_right = CTkFrame(frame)
    label_replace = CTkLabel(frame_right, text="Replace with?", font=("Comic Sans MS", 20, "bold"), fg_color="#202bfe", padx=5, pady=5, corner_radius=20)
    label_replace.pack(pady=(10, 0))

    f_name_replace = CTkEntry(frame_right, placeholder_text="First name", font=("Comic Sans MS", 20, "bold"), corner_radius=5, width=300)
    f_name_replace.pack(pady=(20, 5), padx=20)

    l_name_replace = CTkEntry(frame_right, placeholder_text="Last name", font=("Comic Sans MS", 20, "bold"), corner_radius=5, width=300)
    l_name_replace.pack()

    call_num_replace = CTkEntry(frame_right, placeholder_text="Phone", font=("Comic Sans MS", 20, "bold"), corner_radius=5, width=300)
    call_num_replace.pack(pady=20)
    frame_right.grid(row=1, column=1, padx=(25, 0))

    frame.pack()

    frame_btn = CTkFrame(edit_window, fg_color="#242424")
    btn_cancel = CTkButton(frame_btn, text="Cancel", font=("Comic Sans MS", 20, "bold"), corner_radius=20, width=100, fg_color="#202bfe", command=out)
    btn_cancel.grid(pady=(0, 20), row=0, column=0, padx=(0, 3))

    btn_save = CTkButton(frame_btn, text="Edit", font=("Comic Sans MS", 20, "bold"), corner_radius=20, width=100, fg_color="#202bfe", command=edit)
    btn_save.grid(pady=(0, 20), row=0, column=1, padx=(3, 0))

    frame_btn.pack(pady=10)


#=======================================================================================================================
def delete_contacts():
    root.withdraw()
    delete_window = CTkToplevel(root)
    delete_window.title("Delete contacts")
    delete_window.geometry("450x300")
    delete_window.resizable(False, False)

    def delete():
        id_ = delete_entry.get().strip()
        if not id_:
            CTkMessagebox(title="Error", message="please complete the item!!", width=300, height=150, icon="warning")
            delete_entry.delete(0, END)
        else:
            try:
                msg = CTkMessagebox(title="Delete", message="Are you sure you want to delete?", option_1="Yes", option_2="No", width=300, height=150)
                if msg.get() == "Yes":
                    cursor.execute("delete from contacts where id = ?", (int(id_), ))
                    connection.commit()
                    delete_entry.delete(0, END)
                    refresh_list()
            except:
                CTkMessagebox(title="Error", message="The ID not in contacts!", width=300, height=150, icon="warning")
                delete_entry.delete(0, END)

    def out():
        msg = CTkMessagebox(title="Warning", message="Are you sure you want to Exit?", option_1="Yes", option_2="No", width=300, height=150)
        if msg.get() == "Yes":
            delete_window.destroy()
            root.deiconify()


    label_ = CTkLabel(delete_window, text="Delete contacts", font=("Comic Sans MS", 30, "bold"), corner_radius=20, fg_color="#202bfe", padx=10, pady=10)
    label_.pack(pady=20)

    delete_entry = CTkEntry(delete_window, placeholder_text="ID", font=("Comic Sans MS", 20, "bold"), corner_radius=5, width=250)
    delete_entry.pack(pady=10)

    frame_btn = CTkFrame(delete_window, fg_color="#242424")
    btn_cancel = CTkButton(frame_btn, text="Cancel", font=("Comic Sans MS", 20, "bold"), corner_radius=20, width=100, fg_color="#202bfe", command=out)
    btn_cancel.grid(pady=(0, 20), row=0, column=0, padx=(0, 3))

    btn_save = CTkButton(frame_btn, text="Delete", font=("Comic Sans MS", 20, "bold"), corner_radius=20, width=100, fg_color="#202bfe", command=delete)
    btn_save.grid(pady=(0, 20), row=0, column=1, padx=(3, 0))
    frame_btn.pack(pady=10)

#=======================================================================================================================

entry_font = ("Comic Sans MS", 15)
set_appearance_mode("dark")
set_default_color_theme("blue")
root = CTk()
root.title("Contacts")
root.geometry("500x650")
root.resizable(False, False)
try:
    root.iconbitmap("icon.ico")
except:
    pass

frame_top = CTkFrame(root, fg_color="#242424")
search_box = CTkEntry(frame_top, font=entry_font, placeholder_text="Search...", corner_radius=5, width=440)
search_box.grid(columnspan=3, pady=(10, 5))
search_box.bind("<KeyRelease>", search_contacts)

add_btn = CTkButton(frame_top, font=("Comic Sans MS", 15), text="Add contacts", fg_color="#202bfe", corner_radius=5, height=30, hover_color="#010cdf", command=add_contacts)
add_btn.grid(row=1, column=0, padx=5)
edit_btn = CTkButton(frame_top, font=("Comic Sans MS", 15), text="Edit contacts", fg_color="#202bfe", corner_radius=5, height=30, hover_color="#010cdf", command=edit_contacts)
edit_btn.grid(row=1, column=1, padx=5)
delete_btn = CTkButton(frame_top, font=("Comic Sans MS", 15), text="Delete contacts", fg_color="#202bfe", corner_radius=5, height=30, hover_color="#010cdf", command=delete_contacts)
delete_btn.grid(row=1, column=2, padx=5)
frame_top.pack(pady=(0, 10))

scroll = CTkScrollableFrame(root, width=470, height=550, fg_color="#2d2d2d")
scroll.pack()

refresh_list()


root.mainloop()
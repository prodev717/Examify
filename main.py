import tkinter as tk
import proctor
import threading
import time

def show_error_popup(message):
    error_popup = tk.Toplevel(app)
    error_popup.title("Input Error")
    error_popup.geometry("300x150")
    error_popup.configure(bg="#2C3E50")
    error_label = tk.Label(error_popup, text=message, bg="#2C3E50", fg="#ECF0F1", font=("Helvetica", 12))
    error_label.pack(pady=20)
    ok_button = tk.Button(error_popup, text="OK", command=error_popup.destroy, font=("Helvetica", 12, "bold"), bg="#1ABC9C", fg="white")
    ok_button.pack(pady=10)

def show_terms_and_conditions():
    terms_window = tk.Toplevel(app)
    terms_window.title("Terms and Conditions")
    terms_window.attributes('-fullscreen', True) 
    terms_window.configure(bg="#2C3E50")
    terms_frame = tk.Frame(terms_window, bg="#2C3E50")
    terms_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    terms_text = """\
    Terms and Conditions :-
    1.Camera and microphone will be used to monitor exams. 
    Data is processed locally on your device.If suspicious activity is detected, 
    the exam may be ended. 
    Any failure to attend or complete the exam will not be the app’s responsibility.
    2.Video, audio, and exam data are processed according to our Privacy Policy 
    and are not shared without consent, except for exam-related purposes.
    3.Violations may result in account suspension or termination.
    4.Examify is not responsible for failures to attend or complete 
    exams due to device issues.
    5.Maintain a distance 40-70 Cms from the screen for better exam experience 
    without any interruption.
    6.Make sure you sit in a silent room away from any noise disturbances.
    7.You can cry after seeing the questions but make sure the keyboard doesn't 
    get wet as we won't be responsible for any hardware damage.
    8.You can skip the test if you feel like you will fail but don't 
    blame the app after doing so. 
    9.It is crucial to stay within the boundary for a valid test.
    Certainly! Here’s a more professional version of your message:
    10.After selecting "Proceed," you will be directed to a sample camera view where you 
    can check and adjust your position in relation to your surroundings and the defined boundary limits. 
    You will have 15 seconds to make these adjustments. Please ensure that the boundary box remains 
    within the permissible area; if it turns red, it indicates a potential violation.
    11.Terms may change; continued use means acceptance of updates.
    12.Best of luck.

    For questions, contact us at teamx0403@gmail.com
    """
    terms_label = tk.Label(terms_frame, text=terms_text, bg="#2C3E50", fg="#ECF0F1", font=("Arial", 10), justify=tk.LEFT)
    terms_label.pack(pady=20)
    terms_accepted = tk.BooleanVar()
    terms_checkbox = tk.Checkbutton(terms_frame, text="I have read and agree to the Terms and Conditions", variable=terms_accepted, bg="#2C3E50", fg="#ECF0F1", font=("Arial", 12), selectcolor="#34495E")
    terms_checkbox.pack(pady=10)
    proceed_button = tk.Button(terms_frame, text="Proceed", command=lambda: proceed(terms_window, terms_accepted.get()), font=("Arial", 12, "bold"), bg="#28A745", fg="white", state=tk.DISABLED)
    proceed_button.pack(pady=20)
    terms_accepted.trace("w", lambda *args: proceed_button.config(state=tk.NORMAL if terms_accepted.get() else tk.DISABLED))

def proceed(terms_window, accepted):
    global full_name,reg_number,test_link
    if accepted:
        print("Proceeding to the application...")
        terms_window.destroy() 
        app.destroy() 
        proctor.Tapp(test_link,(full_name,reg_number))
        exit()
    else:
        print("You must accept the terms to proceed.")

def submit_form():
    global full_name,reg_number,test_link
    full_name = name_entry.get()
    reg_number = reg_number_entry.get()
    test_link = test_link_entry.get()
    if not full_name or not reg_number or not test_link:
        show_error_popup("⚠️ All fields are mandatory")
        return 
    print(f"Full Name: {full_name}")
    print(f"Registration Number: {reg_number}")
    print(f"Test Link: {test_link}")
    show_terms_and_conditions()

app = tk.Tk()
full_name = None
reg_number = None
test_link = None
app.title("Examify")
app.geometry("400x500")
app.configure(bg="#2C3E50")
app.iconbitmap("favicon.ico")
title_label = tk.Label(app, text="Welcome to Examify", bg="#2C3E50", fg="#ECF0F1", font=("Helvetica", 18, "bold"))
title_label.pack(pady=(20, 10))
border_frame = tk.Frame(app, bg ="#34495E", bd=5, relief="raised")
border_frame.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
form_frame = tk.Frame(border_frame, bg="#2C3E50")
form_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
label_font = ("Helvetica", 12, "bold")
entry_font = ("Helvetica", 12)
tk.Label(form_frame, text="Full Name:", bg="#2C3E50", fg="#ECF0F1", font=label_font).pack(pady=(10, 5))
name_entry = tk.Entry(form_frame, font=entry_font, bg="#34495E", fg="#ECF0F1", insertbackground='white', bd=2, relief="flat", width=30)
name_entry.pack(pady=(0, 10))
tk.Label(form_frame, text="Registration Number:", bg="#2C3E50", fg="#ECF0F1", font=label_font).pack(pady=(10, 5))
reg_number_entry = tk.Entry(form_frame, font=entry_font, bg="#34495E", fg="#ECF0F1", insertbackground='white', bd=2, relief="flat", width=30)
reg_number_entry.pack(pady=(0, 10))
tk.Label(form_frame, text="Test Link:", bg="#2C3E50", fg="#ECF0F1", font=label_font).pack(pady=(10, 5))
test_link_entry = tk.Entry(form_frame, font=entry_font, bg="#34495E", fg="#ECF0F1", insertbackground='white', bd=2, relief="flat", width=30)
test_link_entry.pack(pady=(0, 10))
submit_button = tk.Button(form_frame, text="Take Test", command=submit_form, font=("Helvetica", 12, "bold"), bg="#1ABC9C", fg="white", relief="raised", bd=3)
submit_button.pack(pady=20)
app.eval('tk::PlaceWindow . center')
app.mainloop()

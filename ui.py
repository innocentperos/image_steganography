from ctypes import windll
import json
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from tkinter import scrolledtext, messagebox, dialog
from pathlib import Path
from script import encode, decode


window = tk.Tk()

file_path = None
shown_details = False
file_path_to_extract = None

def resize_image():

    global file_path

    if not file_path:
        messagebox.showinfo("Missing File", "Select a file first")
        return
    
    dialog_window = tk.Toplevel(window)
    dialog_window.title("Resive Image")

    _tab_control = ttk.Notebook(dialog_window)

    aspect_frame = tk.Frame(_tab_control, padx=40, pady=10)
    _tab_control.add(aspect_frame,text="Aspect Ratio")

    # Add widgets to the dialog
    aspect_ratio_label = tk.Label(aspect_frame, text="Aspect Ratio:")
    aspect_ratio_entry = tk.Entry(aspect_frame, width=40)
    aspect_ratio_label.pack(anchor="w")
    aspect_ratio_entry.pack(anchor="w")
    

    resize_frame = tk.Frame(_tab_control, padx=40, pady=10)
    _tab_control.add(resize_frame, text="Manual Size")

    width_label = tk.Label(resize_frame, text="Width:")
    width_label.pack(anchor="w")

    width_entry = tk.Entry(resize_frame, width=40,)
    width_entry.pack(anchor="w")

    height_label = tk.Label(resize_frame, text="Height:")
    height_label.pack(anchor="w")

    height_entry = tk.Entry(resize_frame,  width=40,)
    height_entry.pack(anchor="w")

    _tab_control.pack(expand=1, fill="both")

    

    def resize():

        try:
            height = int(height_entry.get())
            width = int(width_entry.get())

            
            
        except ValueError:
            messagebox.showerror("Invalid Values", "Width and Height most be unsigned integer")
            return
        dialog_window.destroy()


    confirm_btn = tk.Button(dialog_window, text="Ok", command=resize)
    confirm_btn.pack(anchor="n")

def rotate_image():

    global file_path

    if not file_path:
        messagebox.showinfo("Missing File", "Select a file first")
        return
    
    dialog_window = tk.Toplevel(window, width=200, height=200)
    dialog_window.geometry("300x150")
    dialog_window.title("Rotate Image")

    # Add widgets to the dialog
    label = tk.Label(dialog_window, text="Angle:", anchor="w")
    label.pack(anchor="w")

    angle = tk.Entry(dialog_window,)
    angle.pack( anchor="w")


def select_image():
    global file_path, shown_details



    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", ("*.png","*.jpg","*.jpeg"))],
    )

    if file_path:

        original_file_name = Path(file_path).name
        extension = Path(original_file_name).suffix[1:]
        image = Image.open(file_path)

        img_size = image.size
        aspect = img_size[0] / img_size[1]

        if img_size[0] < img_size[1]:

            image = image.resize(
                ( 500, int(500 * aspect)), Image.Resampling.LANCZOS
            )  # Resize the image if needed
        else:
            image = image.resize(
                (int(500 * aspect), 500), Image.Resampling.LANCZOS
            ) 

        photo = ImageTk.PhotoImage(image)
        image_viewer.configure(image=photo)
        image_viewer.image = (
            photo  # Store a reference to prevent image garbage collection
        )

        # Update the image details
        file_location_label.config(text="File Location: " + file_path)
        image_format_label.config(text="Image Format: "+extension)
        image_size_label.config(
            text="Image Size: {} x {} pixels".format(img_size[0], img_size[1])
        )

        # Show the text input field

        if not shown_details:
            message_label.pack(anchor="w")
            message_entry.config(height=image_viewer.winfo_height(), width=100)
            message_entry.pack()

            secret_label.pack(
                anchor="w",
                pady=(20, 0),
            )
            secret_key.pack(anchor="w")

            shown_details = True

            hide_message_button.pack(anchor="w", pady=(20, 0))


def select_image_to_extract():
    global file_path_to_extract
    file_path_to_extract = filedialog.askopenfilename(
        filetypes=[("Image files",("*.jpeg","*.jpg","*.png"))],
    )

    if file_path_to_extract:

        original_file_name = Path(file_path_to_extract).name
        extension = Path(original_file_name).suffix[1:]
        image = Image.open(file_path_to_extract)

        img_size = image.size
        aspect = img_size[0] / img_size[1]
        image = image.resize(
            (int(500 * aspect), 500), Image.Resampling.LANCZOS
        )  # Resize the image if needed
        photo = ImageTk.PhotoImage(image)
        extract_image_viewer.configure(image=photo)
        extract_image_viewer.image = (
            photo  # Store a reference to prevent image garbage collection
        )

        # Update the image details
        extract_file_location_label.config(text="File Location: " + file_path_to_extract)
        extract_image_format_label.config(text="Image Format: "+extension)
        extract_image_size_label.config(
            text="Image Size: {} x {} pixels".format(img_size[0], img_size[1])
        )

        extract_secret_label.pack(
            anchor="w",
            pady=(20, 0),
        )
        extract_secret_key.pack(anchor="w")

        extract_button.pack(pady=20, anchor="w")

    select_button.pack(anchor="w", pady=(20, 0))



def hide_message():
    global file_path
    original_file_name = Path(file_path).name
    extension = Path(original_file_name).suffix[1:]

    message_to_hide = message_entry.get(index1="1.0", index2= "end-1c").strip()

    print(message_to_hide)
    password = secret_key.get()

    if not message_to_hide or message_to_hide == "":
        messagebox.showerror("Message Required", "Please enter the message you wish to hide into the image.")
        return
    if not file_path:
        messagebox.showerror("Image Required", "Please select the image you want to hide the message into")
        return
    
    if not password:
        response = messagebox.askyesno("Hide without Secret Key", "Are you sure you want to hide the message without using a password")
        if not response:
            return
        password = None
        
    file_to_save = filedialog.asksaveasfilename(
        filetypes=[ ("Image File", f"*.png")],
        defaultextension="png",
        initialfile=f"{original_file_name}_secured",
    )

    if not file_to_save:
        messagebox.showerror("Error", "Please provide the file to save the newly generated image")
        return
    
    if Path(file_to_save).suffix.lower() != ".png":
        messagebox.showerror("Unsupport Export FOrmat", "Please the file to save the newly generated image most be of png format")
        return
    
    try:
        encode(file_path, message_to_hide, file_to_save, password=password, format = "jpeg" if extension == "jpg" else extension)
        messagebox.showinfo("Message Hide", "Message was successfully hidden into the image")
    except Exception as e:
        error = str(e)
        messagebox.showerror("Error Embedding Message", f"Error occured will imbedding message into image, \r\n Reason: \r\n {error}")
    pass

def extract_message():
    password = extract_secret_key.get()
    message = decode(file_path_to_extract, password)

    try:
        content = json.loads(message)

        if "password" in content and content["password"]!= None and content["password"].strip() != password.strip():
            messagebox.showerror("Eror Extracting", "Security key was incorrect")
            return 
        
        messagebox.showinfo("Extracted Message", content["message"])
        extracted_message.replace(index1="1.0", index2="end-1c", chars=content["message"]) 
        extracted_message.pack(anchor="w")


    except Exception as error:
        messagebox.showerror("Eror Extracting", "Could not extract any thing out of this image, either imag was temped or corrupted")

        print(error)
    
    pass

# Create the main window

# Set the window to full-screen initially

window.title("UI Application")
# Create a menu bar
menu_bar = tk.Menu(window)
menu_bar.add_cascade(
    label="Settings",
)

# Add the menu bar to the window
window.config(menu=menu_bar)

# Create the tab control
tab_control = ttk.Notebook(window)

# Create the first tab
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Hide Message")

# Create a frame for the first column
column1 = ttk.Frame(tab1)
column1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Create an image viewer
image_viewer = ttk.Label(column1, anchor="w")
image_viewer.pack()

# Create a frame for the second column
column2 = ttk.Frame(tab1)
column2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Create labels to display image details
file_location_label = ttk.Label(column1, anchor="w")
file_location_label.pack(pady=5, anchor="w")
image_format_label = ttk.Label(column1, anchor="w")
image_format_label.pack(anchor="w")
image_size_label = ttk.Label(column1, anchor="w")
image_size_label.pack(anchor="w")

row2 = ttk.Frame(tab1)
row2.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
# Create a button to select an image
select_button = ttk.Button(row2, text="Select Image", command=select_image)
select_button.grid(padx=(0,20), row=0, column=0)

# resize_btn = ttk.Button(row2, text="Resize", command= resize_image)
# resize_btn.grid(row=0, column=1)

# rotate_btn = ttk.Button(row2, text="Rotate", command= rotate_image)
# rotate_btn.grid(row=0, column=2)


# Create a label and multi-line text input field for the message to hide
message_label = ttk.Label(column2, text="Message to Hide", anchor="w")
message_label.pack(pady=5)
message_entry = scrolledtext.ScrolledText(column2, width=100, height=10, wrap=tk.WORD)
message_entry.pack(pady=16)
secret_label = ttk.Label(column2, text="Secret Word/Password", anchor="w")
secret_key = ttk.Entry(column2, width=50)

secret_label.pack(pady=5, anchor="w")
secret_key.pack(anchor="w")
secret_key.pack_forget()
secret_label.pack_forget()

# Create a button to hide message
hide_message_button = ttk.Button(column2, text="Hide Message", command=hide_message)
hide_message_button.pack_forget()

# Hide the text input field initially
message_entry.pack_forget()
message_label.pack_forget()

# Create the second tab
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Extract Message")

'''
For TAB 2
'''


# Create a frame for the first column
extract_column1 = ttk.Frame(tab2)
extract_column1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a button to select an image
extract_select_button = ttk.Button(extract_column1, text="Select Image to Extract From", command=select_image_to_extract)
extract_select_button.pack(pady=10, anchor="w")

# Create an image viewer
extract_image_viewer = ttk.Label(extract_column1, anchor="w")
extract_image_viewer.pack()

# Create a frame for the second column
extract_column2 = ttk.Frame(tab2)
extract_column2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Create labels to display image details
extract_file_location_label = ttk.Label(extract_column1, anchor="w")
extract_file_location_label.pack(pady=5, anchor="w")
extract_image_format_label = ttk.Label(extract_column1, anchor="w")
extract_image_format_label.pack(anchor="w")
extract_image_size_label = ttk.Label(extract_column1, anchor="w")
extract_image_size_label.pack(anchor="w")

extract_secret_label = ttk.Label(extract_column1, text="Secret Word/Password", anchor="w")
extract_secret_key = ttk.Entry(extract_column1, width=50)

extracted_message_label = ttk.Label(extract_column2, anchor="w", text="Extracted Message:")
extracted_message_label.pack()
extracted_message = scrolledtext.ScrolledText(extract_column2, width=100, wrap=tk.WORD)
extracted_message.pack_forget()

extract_button = ttk.Button(extract_column1, text="Extract Message", command=extract_message)
extract_button.pack(pady=10, anchor="w")
extract_button.pack_forget()

# Pack the tab control
tab_control.pack(expand=1, fill="both")

# Start the main event loop
window.mainloop()

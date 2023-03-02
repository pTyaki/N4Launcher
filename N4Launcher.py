import subprocess
import os
import json 
import customtkinter
from PIL import Image

#Load from config
with open ('config.json', 'r') as f:
    config = json.load(f)

#n4FolderPath = 'C:\\Niagara'
n4FolderPath = config['niagaraDirectory']
items = os.listdir(n4FolderPath)
versionList = []

#Search for items in directory and put them into List
for item in items:
    tempItem = os.path.join(n4FolderPath,item)

    if os.path.isdir(tempItem):
        if item[0:8] == "Niagara-":
            versionList.append(item)
        elif item[0:4] == "EC-N":
            versionList.append(item)

#Select initial value for option box
if config['selectionHist'] not in versionList:
    n4Selection = versionList[0]
else:
    n4Selection = config['selectionHist']


#initiallize the GUI
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("500x350+640+250")
root.title("N4 Launcher (Beta v0.5.2)")

#Function of the GUI
def launch():

    #Disable button to prevent double input
    button.state='disabled'

    #Get the selected option
    n4Selection = optionbox.get()
    config['selectionHist'] = n4Selection
    
    #Define the paths to open the plat and wb
    selectionPath = n4FolderPath + '\\' + n4Selection
    platPath = selectionPath + r'\bin\plat.exe'
    wbPath = selectionPath + r'\bin\wb.exe'

    #Open the plat.exe and installdaemon command
    result = subprocess.run([platPath, 'installdaemon'], capture_output=True)
    print(f"output:\n{result.stdout.decode('utf-8')}")

    #Open the wb.exe
    subprocess.Popen(wbPath, creationflags=subprocess.CREATE_NO_WINDOW)

    #Save the changes onto config file
    with open('config.json', 'w') as f:
        json.dump(config, f)

    #Button state 
    button.state='normal'

    #Error window
    if result.returncode != 0:
        error_window = customtkinter.CTkToplevel()
        error_window.geometry("550+200")
        error_window.title('Warning: Daemon failed')
        error_label = customtkinter.CTkLabel(error_window, text=f"Please check for \"Run as Administrator\"\n\n{result.stdout.decode('utf-8')}")
        error_label.pack(padx=30, pady=30)
        error_window.attributes("-topmost", True)
    else:
        root.quit()


frame = customtkinter.CTkFrame(master = root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

logo = customtkinter.CTkImage(dark_image=Image.open("n4Logo.png"), size=(350,111))
logoButton = customtkinter.CTkLabel(master=frame, image=logo, text="")
logoButton.pack(pady=30, padx=30)

# label = customtkinter.CTkLabel(master=frame, text="niagara", font=("Calibri", 80))
# label.pack(pady=15, padx=30)

button = customtkinter.CTkButton(master=frame, text="LAUNCH", command=launch, font=("Arial Rounded MT Bold", 18), height=40, width=200)
button.pack(pady=10, padx=10)

combobox_var = customtkinter.StringVar(value=n4Selection)

optionbox = customtkinter.CTkOptionMenu(master=frame, values = versionList, font=("Calibri", 14), width=200, variable=combobox_var, fg_color="gray", button_color="gray", text_color="white", dropdown_text_color='white', dropdown_fg_color='gray', dropdown_font=('Calibri',14), anchor='center')
optionbox.pack(pady=1, padx=10)

root.mainloop()
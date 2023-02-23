import subprocess
import os
import json 
import customtkinter

with open ('config.json', 'r') as f:
    config = json.load(f)


#n4FolderPath = 'C:\\Niagara'
n4FolderPath = config['niagaraDirectory']
items = os.listdir(n4FolderPath)
versionList = []

for item in items:
    tempItem = os.path.join(n4FolderPath,item)

    if os.path.isdir(tempItem):
        if item[0:9] == "Niagara-":
            versionList.append(item)

if config['selectionHist'] not in versionList:
    n4Selection = versionList[0]
else:
    n4Selection = config['selectionHist']

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("500x350")
root.title("N4 Launcher (Beta v0.4)")

def launch():

    button.state='disabled'
    n4Selection = optionbox.get()

    config['selectionHist'] = n4Selection
    
    selectionPath = n4FolderPath + '\\' + n4Selection

    platPath = selectionPath + r'\bin\plat.exe'
    wbPath = selectionPath + r'\bin\wb.exe'

    #subprocess.run(platPath)
    # process = subprocess.run([platPath, 'installdaemon'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # # subprocess.Popen(wbPath)
    # stdout = process.stdout.decode('utf-8')
    # stderr = process.stderr.decode('utf-8')

    subprocess.run([platPath, 'installdaemon'])
    subprocess.Popen(wbPath, creationflags=subprocess.CREATE_NO_WINDOW)

    with open('config.json', 'w') as f:
        json.dump(config, f)

    button.state='normal'


frame = customtkinter.CTkFrame(master = root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="niagara", font=("Calibri", 80))
label.pack(pady=15, padx=30)

button = customtkinter.CTkButton(master=frame, text="LAUNCH", command=launch, font=("Arial Rounded MT Bold", 18), height=40, width=200)
button.pack(pady=10, padx=10)

combobox_var = customtkinter.StringVar(value=n4Selection)

optionbox = customtkinter.CTkOptionMenu(master=frame, values = versionList, font=("Calibri", 14), width=200, variable=combobox_var, fg_color="gray", button_color="gray", text_color="white", dropdown_text_color='white', dropdown_fg_color='gray', dropdown_font=('Calibri',14), anchor='center')
optionbox.pack(pady=1, padx=10)

root.mainloop()
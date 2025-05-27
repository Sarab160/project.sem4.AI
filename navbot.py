import folium.map
import osmnx as ox
import networkx as nx
import folium
import tkinter as tk
from tkinter import Button, Label, ttk, messagebox
import webbrowser
import threading
import qrcode
import http.server
import socketserver
import os
import socket
from PIL import Image, ImageTk
import qrcode.constants
from flask import Flask, render_template, request
import time
import tkinter.font as tkFont
import customtkinter as ctk
import json
import random
import nltk
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader,TensorDataset
def getlocal_ip():
    try:
        ser=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        ser.connect(("8.8.8.8",80)) #connect google dns
        ip=ser.getsockname()[0]
        ser.close()
        return ip
    except:
        return "127.0.0.1"

local_ip=getlocal_ip()
port=8000

def http_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Handler=http.server.SimpleHTTPRequestHandler
    
    
    with socketserver.TCPServer(("0.0.0.0", port), Handler) as httpd:
        print(f"serving at http://{local_ip}:{port}")
        httpd.serve_forever()
        

serverthread = threading.Thread(target=http_server,daemon=True)
serverthread.start()
ntu=(31.462140256747546, 73.14853656660802)

graph = ox.graph_from_point(ntu,dist=500,network_type="walk",simplify=True)

buildings = {
    
    "Parking":(31.46081717880768, 73.147092820739),
    "Play Ground":(31.461333672941866, 73.14805734079162),
    "NTU Admission office":(31.461562981172438, 73.14829804863288),
    "library":(31.46181627667768, 73.1476341349666),
    "Department of textile Technology":(31.46190271190029, 73.14797306591923),
    "University Auditorium":(31.4619335984168, 73.14831974143283),
    "Rector office":(31.46198736381052, 73.14870463842514),
    "CECA":(31.462070403829756, 73.14829940012471),
    "Weaving Lab":(31.462256389411486, 73.1476910309468),
    "Weaving Department":(31.46209333142246, 73.1477403727427),
    "Garments":(31.46227418692055, 73.1477939677962),
    "Mechanical lab":(31.462218952501416, 73.14748763003652),
    "Knitting Department":(31.46213444529757, 73.14707584760606),
    "Polymer Engineers":(31.462325670460732, 73.14699990255063),
    "School of Engineering and Technology":(31.46268539522329, 73.14757526142752),
    "IT Center":(31.46280872347778, 73.14887970728613),
    "School of Arts and Design":(31.46303434926647, 73.14925274172467),
    "student advisor office":(31.462306660447254, 73.1488045809811),
    "Textile commissioner organization":(31.462233187200482, 73.14969920763079),
    "Dispensary":(31.46292643690325, 73.1496719603786),
    "Cricket ground":(31.463531685835875, 73.14867077101306),
    "Girls Hostel":(31.464066198080545, 73.15013049282585),
    "Females faculty hostel NTU":(31.463737106593715, 73.15000516317625),
    "Masjid":(31.463238786395106, 73.14754245600439),
    "Faisalabad business school (FBS)":(31.46266492968611, 73.14938226847548),
    "New Boys Hostel":(31.46322330048504, 73.1467574917468),
    "Soccer ground":(31.463841622433254, 73.1468785709324),
    "Badminton Ground":(31.46382674860371, 73.14616711287164),
    "Old Boys Hostel":(31.464183719860642, 73.14608689946283),
    "Hockey Ground":(31.461641859695206, 73.14941717009793),
    "Cafeteria":(31.462919041909956, 73.14807458744437),
    "KnowTex Solution":(31.461186185169844, 73.14763237136276),
    "NTU Reserach centre":(31.46115529840744, 73.14772155481016),
    "Open Gym":(31.46337970770594, 73.14731845808372)
    
}

buildingnnodes = {building:ox.distance.nearest_nodes(graph,coords[1],coords[0]) for building,
            coords in buildings.items()}     # buildings to nearest road nodes

def shortestpath(start,end): #shortest path 
    try:
        path = nx.shortest_path(graph,source=buildingnnodes[start],target=buildingnnodes[end],weight="length")
        distance =nx.shortest_path_length(graph,source=buildingnnodes[start],target=buildingnnodes[end],weight="length")
        return path,distance
    except nx.NetworkXNoPath:
        messagebox.showerror("Error"," No Road-Based Path Found!")  # => Error box
        return None,0



def generate_map(open_browser=True):
    start = start_val.get()      #=>tkinter var to get string data like input
    end= end_val.get()
    if not start or not end:
        messagebox.showerror("Error", "Please select both start and destination!")
        return
    if start==end:
        messagebox.showerror("Error"," Source and Destination can not be same!")
        return
    shortest_nodes,distance=shortestpath(start,end)
    
    if not  shortest_nodes:
        return
    
    uni_map = folium.Map(location=ntu,zoom_start=18)
    
    for building, coords in buildings.items():
        if building==start:
            icon_color="green"
        elif building==end:
            icon_color="red"
        else:
            icon_color="blue"
        popup_html = f"<b>{building}</b><br>Lat: {coords[0]:.5f}, Lng: {coords[1]:.5f}"
        folium.Marker(location=coords, popup=folium.Popup(popup_html,max_width=300), 
                    icon=folium.Icon(color=icon_color)).add_to(uni_map)
    
    path_coords=[(graph.nodes[node]['y'],graph.nodes[node]['x']) for node in shortest_nodes]
    # folium.PolyLine(path_coords, color="blue",weight=5,tooltip=f"Distance {distance:.2f} meters").add_to(uni_map)
    if path_coords:
        folium.PolyLine(path_coords, color="blue", weight=5, tooltip=f"Distance {distance:.2f} meters").add_to(uni_map)
    else:
        messagebox.showerror("Error", "Path could not be drawn due to missing coordinates!")

    # Save and Open Map
    
    
    
    for building,coords in buildings.items():
        roadnode=buildingnnodes[building]
        roadcoord=(graph.nodes[roadnode]['y'],graph.nodes[roadnode]['x'])
        folium.PolyLine([roadcoord, coords], color="gray", weight=2, dash_array="5,5").add_to(uni_map)
        
    
    mapfile = "rmap.html"
    uni_map.save(mapfile)
    if open_browser:
        webbrowser.open(mapfile)
    return mapfile
    # mapfile="rmap.html"
    # uni_map.save(mapfile)
    # webbrowser.open(mapfile)

def generate_qrcode():
    mapfile="rmap.html"
    mapfile=generate_map(open_browser=False)
    if not mapfile:
        return
    
    url=f"http://{local_ip}:{port}/{mapfile}"
    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make(fit=True)
    
    
    qrimg=qr.make_image(fill="black",back_color="white")
    qrimg.save("qrcode.png")
    
    qrdisplay=Image.open("qrcode.png")
    qrdisplay=qrdisplay.resize((200,200))
    qrtk_img = ctk.CTkImage(light_image=qrdisplay, dark_image=qrdisplay, size=(200, 200))
    
    qr_label.configure(image=qrtk_img)
    qr_label.image = qrtk_img  

    qr_label.image=qrtk_img
    qr_label.pack(pady=10)
    
    messagebox.showinfo("Qr code Generated","Scan the Qr code to open map!")


def showshortest_path():
    start=start_val.get()
    end=end_val.get()
    if not start or not end:
        messagebox.showerror("Error", "Please select both Start and Destination!")
        return
    
    if start == end:
        messagebox.showerror("Error", "Source and Destination cannot be the same!")
        return 
    
    shortest_nodes, distance=shortestpath(start,end)
    if not shortest_nodes:
        return
    
    timietake=distance/1.4
    inminutes=timietake/60
    
    bold_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
    path_label.configure(text=f"Time taken: {inminutes:.2f} minutes", text_color="white", font=bold_font)

    distance_label.configure(text=f"Total Distance: {distance:.2f} meters", text_color="white")
    

def view_fullmap():
    uni_map = folium.Map(location=ntu,zoom_start=18)
    
    for building,coords in buildings.items():
        popup_html = f"<b>{building}</b><br>Lat: {coords[0]:.5f}, Lng: {coords[1]:.5f}"
        folium.Marker(location=coords,popup=folium.Popup(popup_html,max_width=300),icon=folium.Icon(color="blue")).add_to(uni_map)
    
    fullmapfile="fullmap.html"
    uni_map.save(fullmapfile)
    webbrowser.open(fullmapfile)

def wheather():
    wheatherfile="weather.html"
    webbrowser.open(wheatherfile)

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/map',methods=['POST'])
def map_view():
    latitude=float(request.form['latitude'])
    longitude=float(request.form['longitude'])
    map=folium.Map(location=(latitude,longitude),zoom_start=18)
    live_popup = folium.Popup(f"""
        <b>Your Live Location</b><br>
        Latitude: {latitude:.6f}<br>
        Longitude: {longitude:.6f}
    """, max_width=300)
    folium.Marker(
        [latitude, longitude],
        tooltip="Live Location",
        popup=live_popup,
        icon=folium.Icon(color="red", icon="user")
    ).add_to(map)
    ##folium.Marker([latitude,longitude],popup="You are here",icon=folium.Icon(color="red")).add_to(map)
    if not os.path.exists("templates"):
        os.makedirs("templates")

    map_path = os.path.join("templates", "map.html")
    map.save(map_path)
    return render_template("map.html")

def start_flask():
    app.run(debug=False, use_reloader=False, host="127.0.0.1", port=5000)

def open_browser_once():

    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(2)  
    webbrowser.open_new("http://127.0.0.1:5000/")
def showframe(frame):
    frame.tkraise()

def studentportal():
    url="https://student.ntu.edu.pk/"
    webbrowser.open(url)
def class_timetables():
    url="https://www.ntu.edu.pk/timetable.php"
    webbrowser.open(url)
def notice_board():
    url="https://www.ntu.edu.pk/notice-board.php"
    webbrowser.open(url)
def adm():
    url="https://admissions.ntu.edu.pk/"
    webbrowser.open(url)
def contact():
    url="https://ntu.edu.pk/contact-us.php"
    webbrowser.open(url)
def program_details():
    url="https://ntu.edu.pk/ug-programs.php"
    webbrowser.open(url)


nltk.download('punkt', quiet=True)

all_words = []
tags = []
xy = []

with open("intents.json", "r") as f:
    intents = json.load(f)

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ['?', '.', '!', ',']
all_words = [w.lower() for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

def bag_of_words(tokenized_sentence, words):
    sentence_words = [w.lower() for w in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1.0
    return bag

X_train = []
y_train = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out

input_size = len(all_words)
hidden_size = 8
output_size = len(tags)
model = NeuralNet(input_size, hidden_size, output_size)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

dataset = TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train))
loader = DataLoader(dataset=dataset, batch_size=8, shuffle=True)

num_epochs = 1000
for epoch in range(num_epochs):
    for (words_batch, labels_batch) in loader:
        outputs = model(words_batch)
        loss = criterion(outputs, labels_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

def chatbot_response(sentence):
    sentence = nltk.word_tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = torch.from_numpy(X).unsqueeze(0)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if intent['tag'] == tag:
                return random.choice(intent['responses'])
    else:
        return "I'm not sure how to answer that. Please try asking something else."

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root=ctk.CTk()
root.title("National Textile University of Faisalabad Smart Navigation System with AI chatbot")
root.geometry("1200x800")

home_frame=ctk.CTkFrame(root)
findroute_frame=ctk.CTkFrame(root)
web_frame=ctk.CTkFrame(root)
chat_frame=ctk.CTkFrame(root)
for frame in(home_frame,findroute_frame,web_frame,chat_frame):
    frame.place(relwidth=1,relheight=1)


label = ctk.CTkLabel(home_frame, text="🏫 NTU NAVBOT 🚀", font=ctk.CTkFont(size=22, weight="bold"), text_color="white")
label.pack(pady=20)

label1 = ctk.CTkLabel(home_frame, text="Home Page ", font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
label1.pack(pady=0,padx=10)
left_emoji = ctk.CTkLabel(home_frame, text="🗺️", font=ctk.CTkFont(size=30), text_color="white")
left_emoji.pack(side="left", padx=20)

right_emoji = ctk.CTkLabel(home_frame, text="🗺️", font=ctk.CTkFont(size=30), text_color="white")
right_emoji.pack(side="right", padx=20)


spacer = ctk.CTkFrame(home_frame, height=100, fg_color="transparent")




start_val = tk.StringVar()
end_val = tk.StringVar()

frame=ctk.CTkFrame(master=root,fg_color="white")
frame.pack(pady=10)

button_config = {
    "font": ctk.CTkFont(size=14, weight="bold"),
    "corner_radius": 10,
    "width": 300,
    "height": 45,
    "fg_color": "#28A745",      
    "hover_color": "#218838",   
    "border_color": "#218838", 
}
h_button_config = {
    "font": ctk.CTkFont(size=20, weight="bold"),
    "corner_radius": 12,
    "width": 250,
    "height": 60,
    "fg_color": "#28A745",      
    "hover_color": "#218838",   
    "border_color": "#218838", 
}
W_button_config = {
    "font": ctk.CTkFont(size=17, weight="bold"),
    "corner_radius": 12,
    "width": 300,
    "height": 60,
    "fg_color": "#28A745",      
    "hover_color": "#218838",   
    "border_color": "#218838", 
}
c_button_config = {
    "font": ctk.CTkFont(size=15, weight="bold"),
    "corner_radius": 10,
    "width": 200,
    "height": 40,
    "fg_color": "#28A745",      
    "hover_color": "#218838",   
    "border_color": "#218838", 
}
spacer.pack()
spacer.pack()
spacer.pack()
spacer.pack()
spacer.pack()
spacer.pack()
ctk.CTkButton(home_frame,text="🤖 Chatbot",command=lambda:showframe(chat_frame),**h_button_config).pack(pady=5)
ctk.CTkButton(home_frame, text="🛣️ Find Route", command=lambda:showframe(findroute_frame), **h_button_config).pack(pady=5)
ctk.CTkButton(home_frame, text="🗺️ View Full Map", command=view_fullmap, **h_button_config).pack(pady=5)
ctk.CTkButton(home_frame, text="🌤️ Show Weather", command=wheather, **h_button_config).pack(pady=5)
ctk.CTkButton(home_frame, text="📍 Live Location", command=open_browser_once, **h_button_config).pack(pady=5)

ctk.CTkButton(home_frame, text="🏛️ About NTU", command=lambda:showframe(web_frame), **h_button_config).pack(pady=5)
label_fr = ctk.CTkLabel(findroute_frame, text="🛣️ Find Your Route", font=ctk.CTkFont(size=24, weight="bold"))
label_fr.pack(pady=20)

input_frame = ctk.CTkFrame(findroute_frame)
input_frame.pack(pady=10, padx=20)

ctk.CTkLabel(input_frame, text="📍 Start Location:", font=ctk.CTkFont(size=14), text_color="white").grid(row=0, column=0, padx=10, pady=10)
startmenu = ttk.Combobox(input_frame, textvariable=start_val, values=list(buildings.keys()), state="readonly", width=40,style="black.TCombobox")
startmenu.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(input_frame, text="🎯 Destination:", font=ctk.CTkFont(size=14), text_color="white").grid(row=1, column=0, padx=10, pady=10)
endmenu = ttk.Combobox(input_frame, textvariable=end_val, values=list(buildings.keys()), state="readonly", width=40)
endmenu.grid(row=1, column=1, padx=10, pady=10)



button_frame = ctk.CTkFrame(findroute_frame)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="🚶 Find Route", command=generate_map, **button_config).pack(pady=10)

ctk.CTkButton(button_frame, text="📏 Show Distance of Path", command=showshortest_path, **button_config).pack(pady=5)
ctk.CTkButton(button_frame, text="🔗 Generate QR Code", command=generate_qrcode, **button_config).pack(pady=5)

ctk.CTkButton(button_frame, text="⬅️ Back to Home", command=lambda: showframe(home_frame), **button_config).pack(pady=10)
info_frame = ctk.CTkFrame(findroute_frame)
info_frame.pack(pady=10, padx=20)


distance_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color="black")
distance_label.pack(pady=5)

path_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=12), wraplength=600, justify="left", text_color="black")
path_label.pack(pady=5)

qr_label = ctk.CTkLabel(findroute_frame, text="", font=ctk.CTkFont(size=12), text_color="black")
qr_label.pack(pady=5)
label2 = ctk.CTkLabel(web_frame, text="🏫 NTU Resources and Websites", font=ctk.CTkFont(size=22, weight="bold"), text_color="white")
label2.pack(pady=20)
label3 = ctk.CTkLabel(web_frame, text="Information Center", font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
label3.pack(pady=20)
button_frame2 = ctk.CTkFrame(web_frame)
button_frame2.pack(pady=10)


ctk.CTkButton(button_frame2, text="🎓 Student Portal", command=studentportal, **W_button_config).pack(pady=5)
ctk.CTkButton(button_frame2, text="📅 Class Time-Tables", command=class_timetables, **W_button_config).pack(pady=5)
ctk.CTkButton(button_frame2, text="📋 Notice Board", command=notice_board, **W_button_config).pack(pady=5)
ctk.CTkButton(button_frame2, text="📄 Admission Details", command=adm, **W_button_config).pack(pady=5)
ctk.CTkButton(button_frame2, text="📝 Program Details", command=program_details, **W_button_config).pack(pady=5)
ctk.CTkButton(button_frame2, text="✉️ contact", command=contact, **W_button_config).pack(pady=5)
ctk.CTkButton(button_frame2, text="⬅️ Back to Home", command=lambda: showframe(home_frame), **W_button_config).pack(pady=10)

msg_bg_user = "#4A90E2"
msg_fg_user = "white"
msg_bg_bot = "#E1E1E1"
msg_fg_bot = "black"

# Create chat message bubble
def create_message_bubble(parent, text, is_user=True):
    bubble = ctk.CTkFrame(
        parent,
        fg_color=msg_bg_user if is_user else msg_bg_bot,
        corner_radius=10,
    )
    label = ctk.CTkLabel(
        bubble,
        text=text,
        fg_color="transparent",
        text_color=msg_fg_user if is_user else msg_fg_bot,
        wraplength=400,
        justify="left",
        font=("Arial", 12)
    )
    label.pack(padx=10, pady=5)
    
    
    bubble.pack(anchor="e" if is_user else "w", pady=5, padx=10)
    
    return bubble




# Chat title
ctk.CTkLabel(chat_frame, text="👋 Hey, how i can help you? ", font=("Arial", 18, "bold")).pack(pady=10)


chat_history_frame = ctk.CTkScrollableFrame(chat_frame, width=550, height=300)
chat_history_frame.pack(pady=5, padx=10)


# input_container = ctk.CTkFrame(chat_frame)
# input_container.pack(pady=10, fill="x", padx=10)

# chat_entry = ctk.CTkEntry(input_container)
# chat_entry.pack( fill="x", expand=True, padx=(0, 10))
input_container = ctk.CTkFrame(chat_frame)
input_container.pack(pady=10)

chat_entry = ctk.CTkEntry(input_container, width=400)
chat_entry.pack(pady=(0, 10))  # Space between entry and button




def send_chat():
    question = chat_entry.get().strip()
    if question == "":
        messagebox.showwarning("Warning", "Please enter your question.")
        return
    
    
    create_message_bubble(chat_history_frame, question, is_user=True)
    
    
    answer = chatbot_response(question)
    
    
    create_message_bubble(chat_history_frame, answer, is_user=False)
    
    chat_entry.delete(0, ctk.END)
    
    
    chat_history_frame.scroll_to("bottom")

send_button = ctk.CTkButton(input_container, text="➤ Send", command=send_chat,**c_button_config)
send_button.pack(pady=5)


W_button_config = {"fg_color": "#007ACC", "hover_color": "#005A9E", "text_color": "white", "corner_radius": 8}
ctk.CTkButton(input_container, text="⬅️ Back to Home", command=lambda: showframe(home_frame), **c_button_config).pack(pady=10)
home_frame.tkraise()
root.mainloop()

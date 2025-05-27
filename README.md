🧭 NTU NAVBOT – Smart Campus Navigation System with AI Chatbot
An intelligent, GUI-based navigation system for National Textile University (NTU) integrating real-time map routing, QR code sharing, and a deep learning chatbot.

________________________________________
📌 Features
•	🗺️ Real-time route finding on NTU campus
•	🔗 QR Code map sharing for mobile access
•	📍 Live location tracking via browser
•	🤖 AI-powered chatbot (NLP with PyTorch)
•	📚 Interactive GUI with CustomTkinter
•	🌐 Flask server for map integration
•	🖥️ Full-featured desktop application
________________________________________
🛠️ Technologies Used
Module	Purpose
folium	Map rendering using Leaflet
osmnx, networkx	Graph-based pathfinding
tkinter, customtkinter	Desktop GUI
qrcode, PIL	QR Code generation and display
Flask	Real-time web mapping
PyTorch, nltk	Chatbot using NLP and deep learning
________________________________________
📐 Architecture
•	Frontend (GUI): Built using CustomTkinter, includes multi-frame navigation for route planning, chatbot, weather, and university portals.
•	Backend:
o	🧠 Chatbot: Trained on intents.json with PyTorch.
o	📍 Pathfinding: Shortest path computed with networkx and osmnx.
o	🌐 Flask: Serves live location maps and HTML views.
________________________________________
🛣️ Routing & Mapping
•	Predefined building coordinates are mapped to nearest road nodes using OSMnx.
•	Users select a start and destination from a dropdown.
•	Shortest path (Dijkstra) is shown with distance and estimated time.
•	QR Code generation creates a link to access the route map on any device.
________________________________________
🤖 AI Chatbot
•	NLP preprocessing with nltk.
•	Neural network trained using PyTorch with:
o	CrossEntropyLoss
o	Adam optimizer
o	Tokenized inputs using Bag-of-Words
•	Chat UI allows dynamic question-answer interaction with fallback responses.
________________________________________
🌐 Flask Integration
•	Hosts /map route to show live user location.
•	Auto-launches in browser using webbrowser.
•	http.server serves rmap.html for QR-code access.
________________________________________
📦 Run the App
Prerequisites
pip install folium osmnx networkx flask customtkinter torch nltk qrcode pillow
________________________________________
📚 References
•	Folium Docs
•	OSMnx Docs
•	NetworkX Docs
•	PyTorch Tutorials
•	Tkinter Guide
________________________________________
🚀 Future Improvements
•	✅ GPS integration with mobile support
•	✅ Weather API integration
•	✅ Speech-to-text chatbot interface
•	✅ Firebase real-time friend locator
🧾 Conclusion
•	The NTU NAVBOT system delivers a seamless smart campus navigation experience by combining intelligent pathfinding, QR code sharing, live mapping, and AI-driven chatbot interactions — all within an elegant desktop application. Built with modular, scalable components, it not only enhances usability for students and visitors but also lays the groundwork for future enhancements such as mobile app integration and real-time GPS support.
•	NAVBOT demonstrates how traditional navigation systems can be transformed into powerful, interactive tools tailored for educational institutions. 🎓🗺️


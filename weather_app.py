import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class PinkWeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 1. WINDOW SETTINGS
        self.setWindowTitle("Weather App") 
        self.setGeometry(100, 100, 350, 400) 
        self.setStyleSheet("background-color: #FFE4E1;") # Pink background
        
        # 2. VERTICAL LAYOUT
        layout = QVBoxLayout()
        
        # 3. TITLE LABEL
        self.baslik = QLabel("Weather Forecast App", self) # English Title
        self.baslik.setFont(QFont("Arial", 16, QFont.Bold)) 
        self.baslik.setAlignment(Qt.AlignCenter) 
        self.baslik.setStyleSheet("color: #D87093;") 
        layout.addWidget(self.baslik) 
        
        # 4. CITY INPUT BOX
        self.sehir_input = QLineEdit(self)
        self.sehir_input.setPlaceholderText("Enter city name... (e.g., London)") # English Placeholder
        self.sehir_input.setFont(QFont("Arial", 11))
        self.sehir_input.setStyleSheet("padding: 8px; border: 2px solid #FFB6C1; border-radius: 5px; background-color: white;")
        layout.addWidget(self.sehir_input) 
        
        # 5. BUTTON
        self.buton = QPushButton("Get Weather", self) # English Button Text
        self.buton.setFont(QFont("Arial", 11, QFont.Bold))
        self.buton.setStyleSheet("background-color: #FF69B4; color: white; padding: 10px; border-radius: 5px;")
        self.buton.clicked.connect(self.hava_durumu_getir)
        layout.addWidget(self.buton) 
        
        # 6. TEMPERATURE LABEL
        self.sonuc_sicaklik = QLabel("", self)
        self.sonuc_sicaklik.setFont(QFont("Arial", 36, QFont.Bold)) 
        self.sonuc_sicaklik.setAlignment(Qt.AlignCenter)
        self.sonuc_sicaklik.setStyleSheet("color: #C71585;") 
        layout.addWidget(self.sonuc_sicaklik) 
        
        # 7. DETAILS LABEL
        self.sonuc_detay = QLabel("", self)
        self.sonuc_detay.setFont(QFont("Arial", 12))
        self.sonuc_detay.setAlignment(Qt.AlignCenter)
        self.sonuc_detay.setStyleSheet("color: #DB7093;")
        layout.addWidget(self.sonuc_detay) 
        
        self.setLayout(layout)
        
    def hava_durumu_getir(self):
        # Get user input and trim whitespace
        girilen_sehir = self.sehir_input.text().strip()
        
        # Check if the input field is empty
        if not girilen_sehir:
            QMessageBox.warning(self, "Warning", "Please enter a city name!") # English Warning
            return
            
        # Convert Turkish characters and lowercase the string for API stability
        sehir = girilen_sehir.replace("İ", "I").replace("ı", "i").replace("ğ", "g").replace("Ğ", "G").replace("ç", "c").replace("Ç", "C").replace("ş", "s").replace("Ş", "S").replace("ö", "o").replace("Ö", "O").replace("ü", "u").replace("Ü", "U").lower()
        
        # API URL configuration (lang=en means API will return descriptions in English)
        api_key = "bc26d290bedde28074c4bf1a809cc169" 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=en"
        
        try:
            # Send HTTP request
            cevap = requests.get(url)
            veri = cevap.json() 
            
            # Check if response is successful
            if veri["cod"] == 200: 
                sicaklik = veri["main"]["temp"] 
                aciklama = veri["weather"][0]["description"] 
                nem = veri["main"]["humidity"] 
                
                # Update GUI with fetched data 
                self.sonuc_sicaklik.setText(f"{int(sicaklik)}°C")
                self.sonuc_detay.setText(f"Condition: {aciklama.capitalize()}\nHumidity: {nem}%")
            else:
                QMessageBox.critical(self, "Error", "City not found! Please check the spelling.") # English Error
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", "Could not connect to the internet!") # English Error

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = PinkWeatherApp()
    pencere.show() 
    sys.exit(app.exec_())
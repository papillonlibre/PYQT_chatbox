import sys
import os
import threading, traceback
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, pyqtSlot
import time
from PyQt5.QtGui import QWheelEvent

# Global variables for font family and size
FONT_FAMILY = "Times New Roman"
FONT_SIZE = 12

class ChatWindow(QMainWindow):
    update_chat_history = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        # Set up the UI
        self.setWindowTitle('Chat Application')
        self.setGeometry(100, 100, 600, 500)

        # Main widget and layout
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)

        # Text area to display chat messages
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("background-color: #d3e8e8;")  # Set background color
        self.layout.addWidget(self.text_area)

        # Input field for entering messages
        self.input_field = QLineEdit(self)
        self.input_field.returnPressed.connect(self.send_message)  # Connect returnPressed (Enter key) signal to send_message.
        self.input_field.setStyleSheet("background-color: #94c7cb;")  # Set background color
        font = self.input_field.font()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SIZE)
        self.layout.addWidget(self.input_field)

        # Button layout
        button_layout = QHBoxLayout()

        # Send button
        self.send_button = QPushButton('Send message', self)
        self.send_button.clicked.connect(self.send_message)  # Connect clicked signal to send_message
        self.send_button.setStyleSheet("background-color: #7bb8bd;")  # Set background color
        font = self.send_button.font()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SIZE)
        self.send_button.setFont(font)
        button_layout.addWidget(self.send_button)

        # Clear history button
        self.clear_button = QPushButton('Clear history', self)
        self.clear_button.clicked.connect(self.clear_history)  # Connect clicked signal to clear_history
        self.clear_button.setStyleSheet("background-color: #7bb8bd;")  # Set background color
        font = self.clear_button.font()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SIZE)
        self.clear_button.setFont(font)
        button_layout.addWidget(self.clear_button)

        # Add button layout to main layout
        self.layout.addLayout(button_layout)

        # Set the main widget and show the window
        self.setCentralWidget(self.main_widget)
        self.show()

        # Chat history
        self.chat_history = []
        # Load chat history from file
        self.load_chat_history()
        self.save_chat_history()
        self.display_chat_history()
        # Connect the wheel event to the custom zoom method
        # self.text_area.wheelEvent = self.zoom_text_area
        self.text_area.wheelEvent = lambda event: self.zoom_text_area(event) # TODO: is this better?

        
        # Start a separate thread to simulate receiving messages
        self.receive_thread = threading.Thread(target=self.simulate_receive_messages)
        self.receive_thread.daemon = True  # Set the thread as a daemon thread
        self.receive_thread.start()

    def send_message(self):
        message = self.input_field.text()
        if message:
            try:
                self.chat_history.append('You: ' + message)
            except Exception as e:
                print(f"Failure: {e}\n  {traceback.format_exc()}")
            self.display_chat_history()
            self.input_field.clear()

            # Save chat history to file in a separate thread
            save_thread = threading.Thread(target=self.save_chat_history)
            save_thread.start()
    # @pyqtSlot(list)
    def display_chat_history(self):
        self.text_area.clear()
        font = self.text_area.font()
        font.setFamily(FONT_FAMILY)
        font.setPointSize(FONT_SIZE)
        self.text_area.setFont(font)

        for message in self.chat_history:
            self.text_area.append(message)

    def load_chat_history(self):
        if os.path.exists('chat_history.txt'):
            with open('chat_history.txt', 'r') as file:
                self.chat_history = file.read().splitlines()

    def save_chat_history(self):
        with open('chat_history.txt', 'w') as file:
            file.write('\n'.join(self.chat_history))

    def simulate_receive_messages(self):
        while True:
            # Simulate a delay between receiving messages
            time.sleep(20)
            received_message = 'Friend: New message'
            self.chat_history.append(received_message)
            self.update_chat_history.emit(self.chat_history)
            # Save chat history to file in a separate thread
            save_thread = threading.Thread(target=self.save_chat_history)
            save_thread.start()

    def clear_history(self):
        self.chat_history = []
        self.display_chat_history()
        # Save chat history to file in a separate thread
        save_thread = threading.Thread(target=self.save_chat_history)
        save_thread.start()
    
    def zoom_text_area(self, event: QWheelEvent):
        # Check if the Ctrl key is pressed to perform zoom
        if event.modifiers() & Qt.ControlModifier:
            # Get the current font size
            current_font = self.text_area.font()
            current_font_size = current_font.pointSizeF()

            # Calculate the zoom factor based on the scroll direction
            zoom_factor = 1.2 if event.angleDelta().y() > 0 else 0.8

            # Calculate the new font size after zooming
            new_font_size = current_font_size * zoom_factor

            # Ensure the new font size is greater than 0
            if new_font_size > 0:
                # Set the new font size for the text area
                new_font = current_font
                new_font.setPointSizeF(new_font_size)
                self.text_area.setFont(new_font)

                # Print the updated font size
                print(f"Updated Font Size: {new_font_size}")

        # Prevent the default scrolling behavior
        event.accept()


    import traceback

    def closeEvent(self, event):
        return super().closeEvent(event)

if __name__ == "__main__":
    # Create the application
    app = QApplication([])

    # Create the main window
    window = ChatWindow()

    # Connect the update_chat_history signal to display_chat_history slot
    window.update_chat_history.connect(window.display_chat_history)
    app.aboutToQuit.connect(app.quit)

    # Start the application event loop
    sys.exit(app.exec_())

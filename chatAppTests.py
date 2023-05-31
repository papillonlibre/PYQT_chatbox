import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from chatApp import ChatWindow

app = QApplication(sys.argv)

class ChatAppTest(unittest.TestCase):
    def setUp(self):
        self.window = ChatWindow()

    def tearDown(self):
        self.window.close()

    def test_send_message(self):
        message1 = "Hello, World!"
        message2 = "World has been greeted"
        input_field = self.window.input_field
        send_button = self.window.send_button

        # Enter the message in the input field
        QTest.keyClicks(input_field, message1)
        QTest.keyPress(input_field, Qt.Key_Enter)

        QTest.keyClicks(input_field, message2)
        QTest.keyPress(input_field, Qt.Key_Enter)

        # Verify if the message is displayed in the chat history
        chat_history = self.window.chat_history
        self.assertTrue(f"You: {message1}" in chat_history)
        self.assertTrue(f"You: {message2}" in chat_history)

    def test_clear_history(self):
        input_field = self.window.input_field
        clear_button = self.window.clear_button

        # Enter a message in the input field
        QTest.keyClicks(input_field, "Test message")

        # Click the clear button
        QTest.mouseClick(clear_button, Qt.LeftButton)

        # Verify if the chat history is cleared
        chat_history = self.window.chat_history
        self.assertEqual(len(chat_history), 0)

    def test_send_empty_message(self):
        input_field = self.window.input_field
        send_button = self.window.send_button

        # Press Enter without entering any message
        QTest.keyPress(input_field, Qt.Key_Enter)

        # Verify that the chat history remains empty
        chat_history = self.window.chat_history
        self.assertEqual(len(chat_history), 0)

    def test_clear_empty_history(self):
        clear_button = self.window.clear_button

        # Click the clear button when the chat history is empty
        QTest.mouseClick(clear_button, Qt.LeftButton)

        # Verify that the chat history remains empty
        chat_history = self.window.chat_history
        self.assertEqual(len(chat_history), 0)

    def test_load_empty_chat_history(self):
        # Set an empty chat history file
        with open('chat_history.txt', 'w') as file:
            file.write('')

        # Reload the chat history
        self.window.load_chat_history()

        # Verify that the chat history is empty
        chat_history = self.window.chat_history
        self.assertEqual(len(chat_history), 0)

    def test_zoom_text_area(self):
        # Get the text area widget from the chat window
        text_area = self.window.text_area
        

        # Set the initial font size
        # initial_font_size = text_area.font().pointSizeF()
        initial_font_size = 10
        print(f"Initial Font Size: {initial_font_size}")
        # Simulate a scroll up event
        wheel_event = QtGui.QWheelEvent(
            QtCore.QPointF(text_area.rect().center()),  # pos
            QtCore.QPointF(text_area.rect().center()),  # globalPos
            QtCore.QPoint(0, 0),  # pixelDelta
            QtCore.QPoint(0, 240),  # angleDelta (120 represents scrolling up)
            QtCore.Qt.NoButton,  # buttons
            QtCore.Qt.NoModifier,  # modifiers
            QtCore.Qt.ScrollUpdate,  # phase
            False,  # inverted
            QtCore.Qt.MouseEventNotSynthesized  # source
        )
        QApplication.sendEvent(text_area, wheel_event)
        
        updated_font_size = text_area.font().pointSizeF()
        print(f"Updated Font Size: {updated_font_size}")

        # Check if the font size decreased after scrolling up
        self.assertTrue(text_area.font().pointSizeF() > initial_font_size)

        # Simulate a scroll down event
        wheel_event = QtGui.QWheelEvent(
            QtCore.QPointF(text_area.rect().center()),  # pos
            QtCore.QPointF(text_area.rect().center()),  # globalPos
            QtCore.QPoint(0, 0),  # pixelDelta
            QtCore.QPoint(0, -120),  # angleDelta (-120 represents scrolling down)
            QtCore.Qt.NoButton,  # buttons
            QtCore.Qt.NoModifier,  # modifiers
            QtCore.Qt.ScrollUpdate,  # phase
            False,  # inverted
            QtCore.Qt.MouseEventNotSynthesized  # source
        )
        QApplication.sendEvent(text_area, wheel_event)
        
        updated_font_size2 = text_area.font().pointSizeF()
        print(f"Updated Font Size2: {updated_font_size2}")

        # Check if the font size increased after scrolling down
        self.assertTrue(text_area.font().pointSizeF() < initial_font_size)



if __name__ == '__main__':
    unittest.main()

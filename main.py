import sys
import time
import os
import pyautogui
import pyperclip
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QCheckBox, QTimeEdit
)
from PyQt6.QtCore import QTimer, QTime


class WhatsAppScheduler(QWidget):
    def __init__(self):
        super().__init__()

        # UI Setup
        self.setWindowTitle("WhatsApp Scheduler")
        self.setGeometry(200, 200, 450, 450)  # Reduced width

        layout = QVBoxLayout()

        # Contact Input
        self.contact_label = QLabel("📲 Contact Name / Number:")
        self.contact_input = QLineEdit()
        layout.addWidget(self.contact_label)
        layout.addWidget(self.contact_input)

        # Message Input
        self.message_label = QLabel("💬 Message:")
        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(90)  # Increased height
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_input)

        # File Attachment
        self.attachment_label = QLabel("📎 No file selected")
        self.attachment_button = QPushButton("Select Attachment")
        self.attachment_button.clicked.connect(self.select_attachment)
        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_button)

        # Caption Input
        self.caption_label = QLabel("📝 Caption (Optional):")
        self.caption_input = QTextEdit()
        self.caption_input.setFixedHeight(50)  # Increased height
        layout.addWidget(self.caption_label)
        layout.addWidget(self.caption_input)

        # Scheduled Message Checkbox
        self.schedule_checkbox = QCheckBox("Schedule Message")
        self.schedule_checkbox.stateChanged.connect(self.toggle_time_selection)
        layout.addWidget(self.schedule_checkbox)

        # Time Selector (Initially Hidden)
        self.time_label = QLabel("⏰ Select Time:")
        self.time_label.setVisible(False)
        self.time_input = QTimeEdit()
        self.time_input.setVisible(False)
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_input)

        # Countdown Display
        self.countdown_label = QLabel("")
        layout.addWidget(self.countdown_label)

        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        # Variables
        self.attachment_path = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)

    def select_attachment(self):
        """Opens File Manager to select an attachment."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File to Send")
        if file_path:
            self.attachment_path = file_path
            self.attachment_label.setText(f"📎 {os.path.basename(file_path)}")

    def toggle_time_selection(self):
        """Show/Hide time input based on the checkbox."""
        is_checked = self.schedule_checkbox.isChecked()
        self.time_label.setVisible(is_checked)
        self.time_input.setVisible(is_checked)

    def update_countdown(self):
        """Updates the countdown in the UI."""
        now = QTime.currentTime()
        target = self.time_input.time()
        remaining = now.msecsTo(target)

        if remaining <= 0:
            self.timer.stop()
            self.countdown_label.setText("⏰ Time reached! Sending now...")
            self.send_whatsapp_message()
        else:
            seconds_left = remaining // 1000
            self.countdown_label.setText(f"🕒 Sending in {seconds_left} seconds...")

    def handle_send(self):
        """Checks if message is scheduled or sent immediately."""
        if self.schedule_checkbox.isChecked():
            self.timer.start(1000)  # Update every second
        else:
            self.send_whatsapp_message()

    def send_whatsapp_message(self):
        """Sends the WhatsApp message with the selected options."""
        contact = self.contact_input.text().strip()
        message = self.message_input.toPlainText().strip()
        caption = self.caption_input.toPlainText().strip()

        if not contact or not message:
            self.countdown_label.setText("⚠️ Please enter contact and message!")
            return

        # Open WhatsApp
        self.countdown_label.setText("🚀 Opening WhatsApp...")
        try:
            subprocess.run(["explorer.exe", "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"], shell=True)
        except Exception:
            self.countdown_label.setText("❌ Error opening WhatsApp!")
            return

        time.sleep(5)

        # Search for the contact
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.write(contact)
        time.sleep(2)

        pyautogui.press("down")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(2)

        # Send Message
        pyautogui.write(message)
        pyautogui.press("enter")
        time.sleep(1)

        # Send Attachment (if selected)
        if self.attachment_path:
            self.countdown_label.setText("📎 Sending attachment...")

            file_directory, file_name = os.path.split(self.attachment_path)

            pyautogui.hotkey("shift", "tab", presses=3, interval=0.1)
            pyautogui.press("enter")
            time.sleep(2)

            pyautogui.hotkey("alt", "d")
            time.sleep(0.5)
            pyperclip.copy(file_directory)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(1.5)

            pyautogui.hotkey("alt", "n")
            time.sleep(0.5)
            pyperclip.copy(file_name)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(3)

            if caption:
                pyautogui.write(caption)
            pyautogui.press("enter")
            time.sleep(1)

            self.countdown_label.setText("✅ Attachment sent successfully!")

        self.countdown_label.setText("✅ Message sent successfully!")


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhatsAppScheduler()
    window.show()
    sys.exit(app.exec())

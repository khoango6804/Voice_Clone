import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt6 import uic
from PyQt6.QtMultimedia import QMediaPlayer
from function import select_audio
from gradio_client import Client, file


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        import os
        ui_file_path = os.path.join(os.path.dirname(__file__), 'form.ui')

        uic.loadUi(ui_file_path, self)

        self.client = Client("tonyassi/voice-clone")
        self.audio_path = None
        self.player = QMediaPlayer()

        self.text_input = self.findChild(QTextEdit, 'textEdit')  # Ensure text_input is linked correctly

        self.pushButton.clicked.connect(self.select_audio)
        self.pushButton_2.clicked.connect(self.clone_voice)

    def select_audio(self):
        select_audio(self)

    def clone_voice(self):
        try:
            user_text = self.text_input.toPlainText()  # Get text input from QTextEdit
            if not user_text:
                print("Text input is empty")
                return

            if self.audio_path:
                audio_file = file(self.audio_path)
                result = self.client.predict(
                    text=user_text,  # Use the text input from user
                    audio=audio_file,
                    api_name="/predict"
                )
                print(result)
            else:
                print("Audio path is not set")
        except Exception as e:
            print(f"Error during cloning voice: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

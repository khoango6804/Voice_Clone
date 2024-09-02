from PyQt6.QtWidgets import QFileDialog
from gradio_client import Client, file
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import QUrl

def select_audio(self):
    file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.mp3)")
    if file_path:
        self.label_2.setText(f"Selected Audio: {file_path}")
        self.audio_path = file_path

def clone_voice(self):
    if self.audio_path is None:
        self.label_2.setText("Please select a reference audio file.")
        return
    text = self.textEdit.toPlainText()
    if not text:
        self.label_2.setText("Please enter some text.")
        return

    try:
        result = self.client.predict(
            text=text,
            audio=file(self.audio_path),
            api_name="/predict"
        )
        # Select save location
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "Audio Files (*.wav)")
        if save_path:
            # Save the audio file to the selected location
            with open(save_path, 'wb') as f:
                f.write(result)

            # Update label to inform the file is saved
            self.label_2.setText(f"Voice cloned! Saved to: {save_path}")

            # Play the audio
            self.player.setSource(QUrl.fromLocalFile(save_path))
            self.player.play()
    except Exception as e:
        self.label_2.setText(f"Error: {str(e)}")
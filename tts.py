from PyQt5 import QtWidgets, uic
import sys
import os
from utils.tts_utils import speak, get_voices, save_speech
import threading
from utils.infer_cli import vc_single


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('tts.ui', self)
        self.show()

        #text edits
        tts_textbox = self.findChild(QtWidgets.QTextEdit, 'tts_textbox')

        #line edits
        speed_input = self.findChild(QtWidgets.QLineEdit, 'speed_input')
        custom_audio_input = self.findChild(QtWidgets.QLineEdit, 'custom_audio_input')
        model_path_input = self.findChild(QtWidgets.QLineEdit, 'model_path_input')
        index_path_input = self.findChild(QtWidgets.QLineEdit, 'index_path_input')
        transpose_input = self.findChild(QtWidgets.QLineEdit, 'transpose_input')
        output_path_input = self.findChild(QtWidgets.QLineEdit, 'output_path_input')


        #comboboxes
        voice_list  = self.findChild(QtWidgets.QComboBox, 'voice_list')
        method_list = self.findChild(QtWidgets.QComboBox, 'method_list')

        #buttons
        play_btn = self.findChild(QtWidgets.QPushButton, 'play_btn')
        save_btn = self.findChild(QtWidgets.QPushButton, 'save_btn')
        custom_audio_browse = self.findChild(QtWidgets.QPushButton, 'custom_audio_browse')
        model_path_browse = self.findChild(QtWidgets.QPushButton, 'model_path_browse')
        index_path_browse = self.findChild(QtWidgets.QPushButton, 'index_path_browse')
        output_path_browse = self.findChild(QtWidgets.QPushButton, 'output_path_browse')
        clone_btn = self.findChild(QtWidgets.QPushButton, 'clone_btn')


        #radio buttons
        same_audio_radio = self.findChild(QtWidgets.QRadioButton, 'same_audio_radio')
        custom_audio_radio = self.findChild(QtWidgets.QRadioButton, 'custom_audio_radio')

        #label
        log_label = self.findChild(QtWidgets.QLabel, 'log_label')


        #tts functions
        def play():
            play_btn.setEnabled(False)
            log_label.setText("Playing...")
            text = tts_textbox.toPlainText()
            voice = voice_list.currentData()
            speed = int(speed_input.text())
            
            if text == "":
                log_label.setText("Text box is empty!")
                play_btn.setEnabled(True)
                return

            def speak_thread():
                speak(text, speed, voice)
                play_btn.setEnabled(True)
            t1 = threading.Thread(target=speak_thread)
            t1.start()
            log_label.setText("Done! Playing...")
            
        def voice_list_update():
            voices = get_voices()
            for voice in voices:
                voice_list.addItem(voice.name, voice.id)

        def save():
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", '', "WAV ,MP3(*.wav *.mp3)")
            if filename:
                text = tts_textbox.toPlainText()
                voice = voice_list.currentData()
                speed = int(speed_input.text())
                save_speech(text, speed, voice, filename[0])
                log_label.setText("Done! Saved as " + filename[0] + ".")

        #connect buttons
        play_btn.clicked.connect(play)
        save_btn.clicked.connect(save)

        #connect comboboxes
        voice_list_update()



        #cloning functions
        
        custom_audio_input.setEnabled(False)
        custom_audio_browse.setEnabled(False)

        method_list.addItem("pm", "pm")
        method_list.addItem("harvest", "harvest")
        method_list.addItem("crepe", "crepe")

        def custom_audio_radio_clicked():
            custom_audio_input.setEnabled(True)
            custom_audio_browse.setEnabled(True)

        def same_audio_radio_clicked():
            custom_audio_input.setEnabled(False)
            custom_audio_browse.setEnabled(False)

        def custom_audio_browse_clicked():
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", '', "WAV ,MP3(*.wav *.mp3)")
            if filename:
                custom_audio_input.setText(filename[0])

        def model_path_browse_clicked():
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", '', "Model (*.pth)")
            if filename:
                model_path_input.setText(filename[0])

        def index_path_browse_clicked():
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", '', "Index (*.index)")
            if filename:
                index_path_input.setText(filename[0])
        
        def output_path_browse_clicked():
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", '', "WAV ,MP3(*.wav *.mp3)")
            if filename:
                output_path_input.setText(filename[0])
        
        def clone():
            clone_btn.setEnabled(False)
            if same_audio_radio.isChecked():
                if tts_textbox.toPlainText() == "":
                    log_label.setText("Text box is empty!")
                    clone_btn.setEnabled(True)
                    return
                audio = "temp.mp3"
            else:
                audio = custom_audio_input.text()
            model = model_path_input.text()
            index = index_path_input.text()
            output = output_path_input.text()
            method = method_list.currentData()
            transpose = int(transpose_input.text())

            if audio == "":
                log_label.setText("Audio file is empty!")
                clone_btn.setEnabled(True)
                return
            if model == "":
                log_label.setText("Model path is empty!")
                clone_btn.setEnabled(True)
                return
            if index == "":
                log_label.setText("Index path is empty!")
                clone_btn.setEnabled(True)
                return
            if output == "":
                log_label.setText("Output path is empty!")
                clone_btn.setEnabled(True)
                return
            
            if transpose > 12 or transpose < -12:
                log_label.setText("Transpose value must be between -12 and 12")
                clone_btn.setEnabled(True)
                return

            def clone_thread():
                log_label.setText("Cloning...")
                save_speech(tts_textbox.toPlainText(), int(speed_input.text()), voice_list.currentData(), "temp.mp3")
                vc_single(
                    sid=0,
                    input_audio_path=audio,
                    f0_up_key=transpose,
                    f0_file=None,
                    f0_method=method,
                    file_index=index,
                    file_index2="",
                    index_rate=1,
                    filter_radius=3,
                    resample_sr=0,
                    rms_mix_rate=0,
                    model_path=model,
                    output_path=output,
                )
                clone_btn.setEnabled(True)
                log_label.setText("Done!")
            t2 = threading.Thread(target=clone_thread)
            t2.start()

        
        #connect radio buttons
        custom_audio_radio.clicked.connect(custom_audio_radio_clicked)
        same_audio_radio.clicked.connect(same_audio_radio_clicked)


        #connect buttons
        custom_audio_browse.clicked.connect(custom_audio_browse_clicked)
        model_path_browse.clicked.connect(model_path_browse_clicked)
        index_path_browse.clicked.connect(index_path_browse_clicked)
        output_path_browse.clicked.connect(output_path_browse_clicked)
        clone_btn.clicked.connect(clone)




app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
from gtts import gTTS
import playsound
import random
import os

class word_reader_gTTS:
    def __init__(self):
         self.language = 'en-uk'       

    def setup_voice(self):
        # self.language = 'en-uk'
        # elif self.cb_languages.currentText().lower() == 'chinese':
        #     self.language = 'zh-cn'

        if self.language == "zh-cn":
            welcome_sentence = "欢迎来到文字游戏. 选择问题数"
            self.bye_sentence = "谢谢你玩文字游戏. 再见"
        else:
            welcome_sentence = 'Welcome to Word play.   Select the number of questions.'
            self.bye_sentence = "Thank you for playing Word Play. Bye Bye"
        
        # say hello using gTTS
        self.read_word(welcome_sentence)

    def read_word(self, audio_string):
        # usingg gTTS
        tts = gTTS(text = audio_string, lang = self.language)
        r = random.randint(1, 10000000)
        audio_file = os.path.dirname(__file__) + '\\audio-'+str(r) +'.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        os.remove(audio_file)

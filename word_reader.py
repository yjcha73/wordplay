import pyttsx3

class word_reader:
    def __init__(self):
        self.engine = pyttsx3.init()

    def setup_voice(self):

        # voice set-up
        # kr_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_KO-KR_HEAMI_11.0"
        en_f_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        en_m_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        ch_w_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0"

        self.language = "English"
        if self.language == "Chinese":
            self.engine.setProperty('voice', ch_w_voice_id)
            welcome_sentence = "欢迎来到文字游戏. 选择问题数"
        else:
            self.engine.setProperty('voice', en_m_voice_id)
            welcome_sentence = 'Welcome to Word play.   Select the number of questions.'

        self.engine.setProperty('languages', self.language)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 10.0)

    def read_word(self, word):
        self.engine.say(word)
        self.engine.runAndWait()

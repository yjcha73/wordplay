import streamlit as st
import io
import glob
import pandas as pd
# import word_reader as wr
import word_reader_gTTS as wr


# Initializing session_state
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False

if 'sampled' not in st.session_state:
    st.session_state['sampled'] = False

if 'words' not in st.session_state:
    st.session_state['words'] = None

if 'test_words' not in st.session_state:
    st.session_state['test_words'] = None

if 'voice_setup' not in st.session_state:
    st.session_state['voice_setup'] = False

if 'q_num_changed' not in st.session_state:
    st.session_state.q_num_changed = False

if 'spell_submitted' not in st.session_state:
    st.session_state.spell_submitted = []

if 'submitted_now' not in st.session_state:
    st.session_state.submitted_now = ''

if 'is_filtered' not in st.session_state:
    st.session_state.is_filtered = False

if 'list_alphabet' not in st.session_state:
    st.session_state.list_alphabet = []
# if 'show_spell' not in st.session_state:
#     st.session_state.show_spell = False

# voice set-up
reader = wr.word_reader_gTTS()

if not st.session_state.voice_setup:
    reader.setup_voice()
    st.session_state.voice_setup = True

def load_data():
    if st.session_state.fn_word[-3:] == 'txt':
        # st.session_state.words = pd.read_csv(st.session_state.fn_word, sep='|', header=0, index_col='word', usecols=['word','definition','sample_sentences'])
        st.session_state.words = pd.read_csv(st.session_state.fn_word, sep='|', header=0, index_col='word')
    elif st.session_state.fn_word[-4:] == 'json':
        st.session_state.words = pd.read_json(st.session_state.fn_word)
        st.session_state.words.reset_index(inplace=True)
        st.session_state.words.set_index(inplace=True,keys='word')
        st.session_state.words.drop(labels='index', inplace=True, axis=1)
        if 'sample_sentences' not in st.session_state.words.columns:
            st.session_state.words['sample_sentences'] = ''
    st.session_state.data_loaded = True

def filtering():
    if st.session_state.is_filtered:
        temp_words = st.session_state.words
        temp_words['temp'] = temp_words.index.str.lower().str[0:1]
        st.write('temp words: ')
        st.write(temp_words)
        
        idx = ~(st.session_state.words.index.str.lower().str[0:1].isin(['a','b']))
        st.write('list alphabet')
        st.write(st.session_state.list_alphabet)
        st.session_state.words.drop(idx, inplace=True)
        st.session_state.words.drop(labels='temp', axis=1, inplace = True)


def sampling():
    st.session_state.test_words = st.session_state.words.sample(st.session_state.n_question)
    if 'spell_submitted' in st.session_state:
        del st.session_state['spell_submitted']
    st.session_state['spell_submitted'] = [False] * st.session_state.n_question
    reset_user_spell()
    reset_check_spell()
    st.session_state.sampled = True
    st.session_state.submitted_now = ''
    
def false_data_loaded():
    st.session_state.data_loaded = False
    false_sampled()

def false_sampled():
    # sampling()
    st.session_state.sampled = False

def q_num_changed():
    reader.read_word(f"Question number {st.session_state.n_q}, {(st.session_state.test_words.index)[st.session_state.n_q-1]}")
    st.session_state.q_num_changed = True
    # st.session_state.user_spell = ''
    # st.session_state.spell_submitted = False
    if 'spell_submitted' in st.session_state:
        del st.session_state['spell_submitted']
        st.session_state['spell_submitted'] = [False] * st.session_state.n_question
    reset_user_spell()
    reset_check_spell()
    st.session_state['user_spell'] = [''] * st.session_state.n_question

def submit_spell(n):
    st.session_state.submitted_now = n
    (st.session_state.spell_submitted)[n-1] = True
    # st.session_state.test_words.loc[word,'user_input_spell'] = user_spell
    # st.session_state.test_words.loc[word,'spell_tested'] = True

def reset_user_spell():
    for i in range(st.session_state.n_question):
        if f'user_spell_{i+1}' in st.session_state:
            st.session_state[f'user_spell_{i+1}'] = ''

def reset_check_spell():
    st.session_state.check_spell = [0] * st.session_state.n_question

def count_answered():
    n_answered = 0
    for i in range(st.session_state.n_question):
        if st.session_state.spell_submitted[i]:
            n_answered += 1
    # st.write(n_answered / st.session_state.n_question * 100)
    return n_answered / st.session_state.n_question * 100

st.title("Welcome to Word Play")
    
# list of dictionary files (*.txt in the folder)
# dicts = glob.glob("*.txt") + glob.glob("*.json")
dicts = glob.glob("*.json")

# select a dictionary file
st.sidebar.selectbox("Select Word File", dicts, key='fn_word', on_change=false_data_loaded)

if not st.session_state.data_loaded: 
    load_data()

# select beginning alphabets
st.sidebar.checkbox('Do you want specific alphabets?', key = 'is_filtered')

# Input the number of questions
st.sidebar.number_input(label="Number of Questions", min_value=1, max_value=len(st.session_state.words), key = 'n_question', on_change=sampling, value= min(10,len(st.session_state.words)))

# initialize session_state of user_spell
for i in range(1+st.session_state.n_question):
    if f'user_spell_{i+1}' not in st.session_state:
        st.session_state[f'user_spell_{i+1}'] = ''

# initialize session_state.check_spell
if 'check_spell' not in st.session_state:
    st.session_state.check_spell = [0] * st.session_state.n_question

# if st.session_state.fnct == "Word Play":
if st.session_state.data_loaded:
    if st.session_state.is_filtered:
        # temp_df = st.session_state.words.reset_index()
        temp_list = st.session_state.words.index.str.lower().str[0:1].drop_duplicates()
        list_alphabet = st.sidebar.multiselect('Select the beginning alphabets', key = 'list_alphabet', options = list(temp_list))
        filtering()

    # Sampling questions
    if not st.session_state.sampled:
        sampling()
        # test_words = st.session_state.test_words
    st.write(f'{int(count_answered())}%')
    st.progress(int(count_answered())/100)
    # st.sidebar.selectbox("Question Number:", range(1, st.session_state.n_question + 1), on_change=q_num_changed, key = "n_q")

    # word = (st.session_state.test_words.index)[st.session_state.n_q-1]
    # st.header("QUESTION #" + str(st.session_state.n_q))

    for n_q in range(st.session_state.n_question):
        col1, col2, col3, col4, col5 = st.columns([2,3,7,3,2])

        with col1:
            if st.button(f"{n_q+1}", key=f"read_btn_{n_q+1}"):
                reader.read_word(f"Question number {n_q+1}, {(st.session_state.test_words.index)[n_q]}")
                
                st.session_state.submitted_now = n_q + 1 

        with col2: 
            st.text_input("Answer", on_change=submit_spell, kwargs = dict(n=n_q+1), key=f"user_spell_{n_q+1}", 
                            label_visibility='collapsed')
            
        with col3:
            # st.button("Submit", on_click = submit_spell, kwargs = dict(n=n_q+1), key=f'submit_btn_{n_q+1}')
            # if st.session_state.submitted_now != '':
            # n = st.session_state.submitted_now
            st.write(f'{st.session_state.test_words.iloc[n_q].definition}')
            # st.write(f'Sample Sentences: {st.session_state.test_words.iloc[n_q].sample_sentences}')            

        if st.session_state.spell_submitted[n_q]:
            with col4:
                st.write((st.session_state.test_words.index)[n_q])
            with col5:
                if st.session_state[f'user_spell_{n_q+1}'].lower() == (st.session_state.test_words.index)[n_q].lower():
                    st.session_state.check_spell[n_q] = 1
                    st.success("Pass")
                else: 
                    st.session_state.check_spell[n_q] = 0
                    st.error("Fail")
            with col3:
                st.write(f'{st.session_state.test_words.iloc[n_q].sample_sentences}') 
        else:
            with col4:
                st.write((st.session_state.test_words.index)[n_q][0:2])           

    if count_answered()==100:
        st.header(f'Score: {sum(st.session_state.check_spell)}/{st.session_state.n_question}')
        st.write(st.session_state.test_words)



    










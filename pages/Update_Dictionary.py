import streamlit as st
import glob
import os
import pandas as pd
import json

def save_json(df, filename):
    js = df.to_json(orient='records')
    parsed = json.loads(js)
    js_data = json.dumps(parsed, indent=4)
    with open(filename, 'w', ) as outfile:
        outfile.write(js_data)
    # clear()

def init_session_state():
    if 'new_word' not in st.session_state:
        st.session_state.new_word = ''
    if 'new_definition' not in st.session_state:
        st.session_state.new_definition = ''
    if 'new_sentence' not in st.session_state:
        st.session_state.new_sentence = ''

def clear():
    # st.session_state['new_word'] = ''
    # st.session_state['new_definition'] = ''
    # st.session_state['new_sentence'] = ''
    init_session_state()
    del st.session_state['new_word']
    del st.session_state['new_definition']
    del st.session_state['new_sentence']

option = st.radio('Select option', options=['Add','Update','Delete'])
st.title(f'{option} a word')

path = os.path.abspath('.')
st.write(path)

# dics = glob.glob('*.txt') + glob.glob('*.json')
dics = glob.glob('*.json')

dic = st.selectbox('Select the Dictionary', dics)

if dic[-3:] == 'txt':
    words = pd.read_csv(dic, sep='|', header=0)
elif dic[-4:] == 'json':
    words = pd.read_json(dic)
    # words = json.loads(dic)
    # st.write(json.dumps(words))

cols = list(words.columns)
st.write(words)    

if option == 'Add':
    word = st.text_input('word', key='new_word')

    if word in list(words.word):
        st.warning(f'The word {word} already exists in the dictionary.')
    else:    
        definition = st.text_input('definition', key='new_definition')
        sentence = st.text_input('sample sentences', key='new_sentence')
        temp_word = pd.DataFrame([{'word': word, 'definition': definition, 'sample_sentences': sentence}])
        words = pd.concat([words, temp_word])
                
        if st.button('Save', on_click=save_json, args=[words, dic]):
            st.write(f'{dic} is updated.')
        
        clear()

elif option == 'Update':
    word = st.text_input('word', key='new_word')

    if (word not in list(words.word)) & (word !=''):
        st.warning(f'The word {word} is not in the dictionary.')
    else:    
        idx = (words['word'] == word)
        definition = st.text_input('definition', key='new_definition', value=str(words.loc[idx, 'definition'].values).replace("'","").replace('[',"").replace(']',''))
        sentence = st.text_input('sample sentences', key='new_sentence', value=str(words.loc[idx, 'sample_sentences'].values).replace("'","").replace('[',"").replace(']',''))
        words.loc[idx,'definition'] = st.session_state.new_definition
        words.loc[idx,'sample_sentences'] = st.session_state.new_sentence         
        if st.button('Update', on_click=save_json, args=[words,dic]):
            st.write(f'{dic} is updated.')

        clear()

elif option == 'Delete':
    word = st.selectbox('Select a word to delete', options = list(words.word))
    idx = words[words.word == word].index
    st.write(words.loc[idx])
    if st.button('Delete'):
        st.write(idx)
        words.drop(idx, inplace=True)
        save_json(words, dic)
        st.write(f'{word} is deleted from the dictionary {dic}')

    clear()
        
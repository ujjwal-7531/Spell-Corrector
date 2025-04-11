import streamlit as st
import pickle

st.title("✅🔡 Spelling Checker")
with open('dick.pkl', 'rb') as f:
    word_prob = pickle.load(f)

word = st.text_input("Enter a word to check its spelling:")

if word:
    st.write(f"You entered: {word}")

def split(word):
    parts = []
    for i in range(len(word)+1):
        parts += [(word[:i], word[i:])]
    return parts

def delete(word):
    output = []
    for l,r in split(word):
        output.append(l+r[1:])
    return output

def swap(word):
    output = []
    for l,r in split(word):
        if (len(r) > 1):
            output.append(l + r[1] + r[0] + r[2:])
    return output

def replace(word):
    characters = 'abcdefghijklmnopqrstuvwxyz'
    output = []
    for l,r in split(word):
        for char in characters:
            output.append(l + char +  r[1:])
    return output

def insert(word):
    characters = 'abcdefghijklmnopqrstuvwxyz'
    output = []
    for l,r in split(word):
        for char in characters:
            output.append(l + char + r)
    return output

def modify(word):
    return list(set(insert(word)+delete(word)+swap(word)+replace(word)))

def check_spell(word, count = 5):
    output = []
    suggested_words = modify(word)
    for w in suggested_words:
        if w in word_prob:
            output.append([word_prob[w],w])
    output = sorted(output,reverse=True)
    last = []
    for i in range(min(count, len(output))):
        last.append(output[i][1])
    return last

if word:
    suggestions = check_spell(word.lower())
    if suggestions:
        st.write("### 🔍 <span style='font-size:24px;'>Did you mean:</span>", unsafe_allow_html=True)
        cols = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                st.button(suggestion)
    else:
        st.warning("❌ No suggestions found.")
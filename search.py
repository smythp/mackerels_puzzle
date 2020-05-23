import operator
import requests
import pandas as pd



word_list_url = "https://norvig.com/ngrams/word.list"

words_request = requests.get(word_list_url)

words = words_request.text.split('\n')


with open('states.txt', 'r') as states_file:
    imported_states = states_file.readlines()
    
states = {}

# CLean states
for state in imported_states:
    state = state.strip()

    state_no_whitespace = state.replace(' ', '')
    state_lower = state_no_whitespace.lower()
    state_set = set(state_lower)
    states[state] = state_set
    

# # Make state strings into sets of letters
# states = {state: set(list(state)) for state in states}

mackerels = {state: [] for state in states}


word_counter = 0

for word in words:

    mackerel_states = []

    for state in states:
        if len(mackerel_states) > 1:
            break
        
        if not any(character in states[state] for character in word):
            mackerel_states.append(state)

    if len(mackerel_states ) == 1:
        mackerels[mackerel_states[0]].append(word)

    # progress_float = word_counter / len(words)
    # progress_percent = "{:.0%}".format(progress_float)
    # print([m for m in mackerels if mackerels[m]])


tagged_words = {}

for state in mackerels:
    for word in mackerels[state]:
        tagged_words[word] = state


sorted_words = sorted(tagged_words, key=len, reverse=True)

sorted_words_tagged = {word: tagged_words[word] for word in sorted_words}

print('Longest "mackerels":')
s = pd.Series(sorted_words_tagged)
print(s.head(30))

print('States with the most "mackerels:')

s = pd.Series(sorted_words_tagged)

print(s.value_counts().head())

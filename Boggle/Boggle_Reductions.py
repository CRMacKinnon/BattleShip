import pandas as pd
import os
import sys

dir = os.path.dirname(sys.argv[0]) +'/'

word_list_master = pd.read_csv(dir + 'Unfiltered_dictionary_internal.txt',header = None,sep='\t',keep_default_na=False)
word_list_master.columns = ['Words']

alphabet = list('abcdefghijklmnopqrstuvwxyz')
Arg_list = [letter1 + letter2 for letter1 in alphabet for letter2 in alphabet]


word_list = [word for word in word_list_master['Words'] if 16 >= len(word) >=3]
print(word_list)
exit()
# Check first letter of word for captial. Remove as improper noun
for word in word_list[:]:
    if word[0].isupper() == True:
        word_list.remove(word)

# add 17 letter words containing qu in it. As 'Qu' dice counts as two letters
for q_word in word_list_master[:]:
    if 'qu' in q_word:
        if len(q_word) == 17:
            word_list.append(q_word)

# Check through all the words. for letter containing all two letter combinations
# then remove combinations that exist. Needed for in game. Doesnt reduce dictionary
for word in word_list[:]:
    for letter_combo in Arg_list:
        if letter_combo in word:
            Arg_list.remove(letter_combo)

new_boggle =list('AAEEGNABBJOOACHOPSAFFKPSAOOTTWCIMOTUDEILRXDELRVYDISTTYEEGHNWEEINSUEHRTVWEIOSSTELRTTYHIMNUQHLNNRZ')
old_boggle = list('AACIOTABILTYABJMOQACDEMPACELRSADENVZAHMORSBIFORXDENOSWDKNOTUEEFHIYEGKLUYEGINTVEHINPSELPSTUGILRUW')

# Count the number of letter posstion in NEW BOGGLE
new_boggle_dict ={}
for letter in alphabet:
    count= 0
    for dice_letter in new_boggle:
        if letter == dice_letter.lower():
            count+=1
    new_boggle_dict[letter]= count

# Count the number of letter posstion in OLFBOGGLE
old_boggle_dict ={}
for letter in alphabet:
    count= 0
    for dice_letter in old_boggle:
        if letter == dice_letter.lower():
            count+=1
    old_boggle_dict[letter]= count


old_boggle_dict['qu'] = old_boggle_dict.pop('q')
new_boggle_dict['qu'] = new_boggle_dict.pop('q')

for letter in alphabet[:]: # take a letter
    if letter == 'q':break
    for word in word_list[:]: # take a word
        count = 0
        for letters in word: # take the letters from the words
            if letter == letters:
                count +=1
        if count > new_boggle_dict[letter]:
            #print("word: %s\nCount: %s\nletter: %s\nMax: %s\n"%(word,count,letter,new_boggle_dict[letter]))
            word_list.remove(word)

for word in word_list[:]:
    count = 0
    for idx in range(1,len(word))[:]:
        if (word[idx-1]+word[idx]) == 'qu':
            count+=1
    if count > new_boggle_dict['qu']:
        count+=1
        word_list.remove(word)

FINAL_List_of_words = pd.DataFrame(word_list,columns=['Words'])
FINAL_List_of_words.to_csv(dir +'reduced_dictionary.txt',sep='\t',index=False)

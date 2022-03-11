# ----------------------------------------------------
# obtain lemma frequency of the words.
# author: Adrian Avendano.
# e-mail: adavendanon@miners.utep.edu
# ----------------------------------------------------
from tempfile import tempdir
from numpy import append
import pandas as pd
from pkg_resources import to_filename
import stanza

def cal_freq():
    chunk_size = 1000
    nlp = stanza.Pipeline('en')
    files = ['test.csv','SUBTLEX_USfrequency_above1.csv', 'SUBTLEX_USfrequency_above1_2.csv']
    suffix_list = ['ion','sion','er','ment','ant','ent','age','al','ence','ance','ery','ry','ship','ity','ness','cy','ive','ous','ful','less','able','ee', 'or','ly']
    freq = pd.read_csv(files[0], nrows=chunk_size)
    lst_freq = freq.values.tolist()

    csv_data = []
    dict_word = {}
    sub_info = [0,0,0]

    for row in range(len(lst_freq)):
        doc = nlp(lst_freq[row][0])
        dicts = doc.to_dict()
        curr_word = dicts[0][0]['lemma']
        keys = list(dict_word.keys())
        curr_freq = lst_freq[row][1]
        
        for i in range(len(keys)):
            sub_info = obtain_substring(curr_word, keys[i])

        if(sub_info[1] == True):
            curr_freq += dict_word[sub_info[2]] 
            del dict_word[sub_info[2]]
            curr_word = sub_info[0]

        if curr_word not in dict_word:
            dict_word[curr_word] = curr_freq
        else: 
            dict_word[curr_word] += curr_freq
    
    for key in dict_word:
        new_row = []
        new_row.append(key)
        new_row.append(dict_word[key])
        csv_data.append(new_row)
    csv_file = pd.DataFrame(csv_data, columns=['Word', 'FREQcount'])
    csv_file.to_csv('SUBTLEX_USfrequency_above1_result.csv')

def obtain_substring(str1, str2):
    og_string = str1
    key = str2
    if len(str1) > len(str2):
        temp = str2
        str2 = str1
        str1 = temp
    if str1[0] != str2[0]:
        return og_string, False, key
    if len(str1) > 3:
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                return og_string, False, key
        return str1, True, key
    else:
        return [0,0,0]
        

def main():
    cal_freq()

if __name__ == "__main__":
    main()
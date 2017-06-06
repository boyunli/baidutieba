# coding:utf-8

import json
import os

filepath = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(filepath, '3755re.txt')

data = { }


if __name__ == '__main__':

    with open(filename, 'r') as f:
        words = f.readlines()
        for i, word in enumerate(words):
            word = word.strip('\n')
            data[i+1] = word
     
    with open('3755.json', 'w') as jf:
        json.dump(data, jf, indent=4, ensure_ascii=False)

## Importing Libraries
import csv
import json
import re
import os
import pydub
import hazm
from IPython import display

data_dir = 'data/'
formatted_dir = 'formatted/'
file_paths = os.listdir(data_dir)

## Text normalization function
def normalize(input_text):

    """
    Return a normalized persian text

        text : [string] Inputed text
    """
    patterns = [
        ('ي' , 'ی'),
        ('ئ' , 'ی'),
        ('ك' , 'ک'),
        ('ؤ' , 'و'),
        ('ة' , 'ه'),
        ('ۀ' , 'ه'),
        ('ـ' , ''),
        ('[إأآ]' , 'ا'),
        ('[ءًٌٍَُِّ]' , ''),
    ]

    per = '۱۲۳۴۵۶۷۸۹۰'
    eng = '1234567890'
    arb = '١٢٣٤٥٦٧٨٩٠'

    text = input_text

    for to_replace , with_char in patterns:
        text = re.sub(to_replace,with_char,text)

    table_eng = text.maketrans(eng , per)
    table_arb = text.maketrans(arb , per)

    text = text.translate(table_eng)
    text = text.translate(table_arb)

    return text

## Correcting wav files names
for file_path in file_paths:
    
    if file_path.endswith('.wav'):

        new_path = []
        new_path.extend(file_path)
        
        if new_path[3] == 'a':
            continue

        if new_path.count('.') == 2:
            new_path.remove('.')

        new_path.insert(3 , 'a')
        new_path = ''.join(new_path)
        
        os.rename(data_dir + file_path , data_dir + new_path)

## Rereading corrected wav names
file_paths = os.listdir(data_dir)

## Converting wav to mp3
for file_path in file_paths:

    if file_path.endswith('wav'):

        audio = pydub.AudioSegment.from_wav(data_dir + file_path)
        audio.export(formatted_dir + file_path.split('.')[0] + '.mp3' , format='mp3')

## Creating template dictionary for json file
data_dict ={
    'audio' : [],
    'duration' : [],
    'text' : []
}

hazm_normalizer = hazm.Normalizer()

with open('data/Senatelecom.tsv' , encoding='utf-8') as file:
    data = csv.reader(file , delimiter='\t')

    for line in data:
        if (line[1].split('.')[0] + '.wav') in file_paths:

            name = line[1].split('.')[0] + '.wav'

            audio_obj = pydub.AudioSegment.from_wav(data_dir + name)
            duration = audio_obj.duration_seconds

            text = hazm_normalizer.normalize(line[2])
            text = normalize(text)

            data_dict['audio'].append(name)
            data_dict['duration'].append(duration)
            data_dict['text'].append(text)
            
## Creating json file
with open('audio_data.json' , mode='w') as f:
    json.dump(data_dict , f)
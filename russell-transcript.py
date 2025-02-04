import json
import os
import sys

"""Whisper formatting from JSON to txt

This script takes the JSON output file from Whisper transcription and applies formatting changes according to Russell Library's needs, with the intention of uploading authenticated transcripts to Aviary/OHMS.
The idea is that captured diarization formatting in the JSON is reflected in hard returns in the txt file and SPEAKER spots that can be substituted for speaker names with find and replace.


The script uses a sys argv input, so when run from the terminal, the script looks for a directory to be provided after script, e.g. > python 3 [name of script] [target directory]
The script will run on any JSON files in the directory.
The standard text edits requested by the Russell Library are found at the end of the script and can be removed if not needed. 

"""


#set path to file
json_folder = sys.argv[1]   #path to json files

#compile a list of files
json_files = [file for file in os.listdir(json_folder) if file.endswith('.json')]

#construct full path to each json file and read it
for json_file in json_files:
    source_json = os.path.join(json_folder, json_file)
    with open(source_json, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)

#create txt file that will be populated with transcript from json, change "_TS.txt" to your naming convention
    file_name = os.path.splitext(os.path.basename(source_json))[0]
    transcript = os.path.join(os.path.dirname(source_json), file_name + "_TS-parenthesis.txt")
    open(transcript, 'w').close()

    tally = 0
    speaker = None
    previous_word = None
    time_vars = []

#create and insert timestamps, apply formatting/diarization, and populate txt file with formatted transcript
    with open(transcript, "w", encoding='utf-8',errors='ignore') as doc:
        for tally, segment in enumerate(data["segments"]):
            for word in segment["words"]:
                hours = int(word["start"] // 3600)
                minutes = int(word["start"] % 3600 // 60)
                seconds = int(word["start"] % 60)
                formatted_time = f"[{hours:02}:{minutes:02}:{seconds:02}]"
                current_word = word["word"]
                if "SPEAKER" in current_word and current_word != speaker:
                    speaker = current_word
                    paren_speaker = current_word[1:-1]
                    doc.write("\n\n")
                    doc.write(formatted_time)
                    doc.write("\n")
                    doc.write(paren_speaker + ": ")
                elif current_word == " >>":
                    if "01" in speaker:
                        if previous_word is not None and "SPEAKER" in previous_word:
                            doc.write("--")
                        else:
                            speaker = "SPEAKER_00"
                            doc.write("\n\n")
                            doc.write(formatted_time)
                            doc.write("\n")
                            doc.write(speaker + ": --")
                    elif "00" in speaker:
                        if previous_word is not None and "SPEAKER" in previous_word:
                            doc.write("--")
                        else:
                            speaker = "SPEAKER_01"
                            doc.write("\n\n")
                            doc.write(formatted_time)
                            doc.write("\n")
                            doc.write(speaker + ": --")
                elif current_word == speaker:
                    continue  #skip writing speaker's name again
                else:
                    doc.write(current_word)

                previous_word = current_word  #update previous_word for the next iteration

    print('formatting finished\n')

#optional text edits (and optional tracking that currently displays in the terminal window but could be used to create a report), as a sample the following are find and replace edits for a specific project
    replacements = {
        '[BLANK_AUDIO]': '',
        '...': '--',
        ' - ': '',
        'black': 'Black',
        '  ': ' ',
    }

    edits_count = {
        '[BLANK_AUDIO]': 0,
        '...': 0,
        ' - ': 0,
        'black': 0,
        '  ': 0,

    }

    with open(transcript, "r", encoding='utf-8') as doc:
        content = doc.read()
        for edit, replacement in replacements.items():
            if edit in content:
                count = content.count(edit)
                content = content.replace(edit, replacement)
                edits_count[edit] += count

    for edit, count in edits_count.items():
        print(f"{edit}: {count} changes")

    with open(transcript, "w", encoding='utf-8') as doc:
        doc.write(content)

    print('\nediting finished')
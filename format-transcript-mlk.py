import json
import os

"""[script title]

[script abstract]


this script is currently set up to run the formatting on multiple json files, but can accommodate single use by de-indenting, removing the for loop, assigning json_file instead of json_files, and ensuring source_json constructs based on these variables

-text editing is separate script
-sys.arg to create paths in terminal

[how to use]



"""

#set path to file
json_folder = "C:\\Users\\chrislot\\Documents\\test-files\\mlk-transcript"#path to json files

#compile a list of files
json_files = [file for file in os.listdir(json_folder) if file.endswith('.json')]

#construct full path to each json file and read it
for json_file in json_files:
    source_json = os.path.join(json_folder, json_file)
    with open(source_json, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)

#create txt file that will be populated with transcript from json, change "_TS.txt" to your naming convention
    file_name = os.path.splitext(os.path.basename(source_json))[0]
    transcript = os.path.join(os.path.dirname(source_json), file_name + "_TS.txt")
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
                    doc.write("\n\n")
                    doc.write(formatted_time)
                    doc.write("\n")
                    doc.write(speaker + ": ")
                elif current_word == " >>":
                    if "01" in speaker:
                        if previous_word is not None and "SPEAKER" in previous_word:
                            doc.write("--")
                        else:
                            speaker = "(SPEAKER_00)"
                            doc.write("\n\n")
                            doc.write(formatted_time)
                            doc.write("\n")
                            doc.write(speaker + ": --")
                    elif "00" in speaker:
                        if previous_word is not None and "SPEAKER" in previous_word:
                            doc.write("--")
                        else:
                            speaker = "(SPEAKER_01)"
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
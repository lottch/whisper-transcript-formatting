import json
import os

#set path to file
json_folder = "C:\\Install\\Chris-Lott-dock\\Documents\\digital asset coordinator\\russell-transcripts\\20241021-batch\\addition"
json_files = [file for file in os.listdir(json_folder) if file.endswith('.json')]
for json_file in json_files:
    # Construct the full path to the JSON file
    source_json = os.path.join(json_folder, json_file)
    with open(source_json, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)

#create txt file that will be populated with transcript from json
    file_name = os.path.splitext(os.path.basename(source_json))[0]
    transcript = os.path.join(os.path.dirname(source_json), file_name + "_TS.txt")
    open(transcript, 'w').close()

    tally = 0
    speaker = None
    previous_word = None
    time_vars = []

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
                    continue  # Skip writing speaker's name again
                else:
                    doc.write(current_word)

                previous_word = current_word  # Update previous_word for the next iteration

    print('formatting finished\n')

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

        # add other considerations

    for edit, count in edits_count.items():
        print(f"{edit}: {count} changes")

    with open(transcript, "w", encoding='utf-8') as doc:
        doc.write(content)

    print('\nediting finished')
# Whisper Staging Walkthrough
(This walkthrough is for UGA Libraries users with access to the OpenAI Whisper development server)
<br/>

The Whisper development server GUI is a pretty straightforward interface, but it's important to use with the appropriate settings.
<br/>
![Screenshot 2025-02-07 163833](https://github.com/user-attachments/assets/9e5b0b5e-622c-4a7f-b024-b5775280e950)
<br/>Model: Large V2
<br/>
Language: English
<br/>--There is functionality for different languages (and a version of the formatting script can be adapted for any language simply by modifying the word 'SPEAKER' in the script), Whisper will auto-detect language but to ensure accuracy it's best to indicate language. 
<br/>
URL: This is an option if you want to transcribe from a URL instead of a file
<br/>

![Screenshot 2025-02-06 144142](https://github.com/user-attachments/assets/bb966ca0-ad5c-4fbd-b297-a6e357cc4086)

Task: transcribe</br>
VAD: silero-vad</br>
VAD - Merge Window (s): 5</br>
VAD - Max Merge Size (s): 30</br>
**when planning to use the formatting script make sure to check the boxes on Word Timestamps, Word Timestamps - Highlight Words, and Diarization**

![Screenshot 2025-02-06 144426](https://github.com/user-attachments/assets/6b2e00e3-c8b4-44ce-afa1-abce9c31c6dd)

Once the file(s) have finished transcribing, the transcript shows in the preview window and the transcript files can be downloaded in the file formats shown above. For the purposes of using the formatting script, the JSON file needs to be downloaded, and any of the other formats as need be.

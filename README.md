# An advanced file conveter
# Description
My first side project with using python. <br />
And this is my first time to user github. <br />
This is a file conveter with image conveter, audio conveter, video conveter and document conveter.

# Support format
Image: "PNG", "JPG", "JPEG", "ICO", "BMP", "WEBP", "HEIC", "HEIF" <br />
Audio: "MP3", "WAV", "AAC", "M4A", "OGG", "WMA", "FLAC" (The Audio converter also support video to audio) <br />
Video to Audio: "MP4", "AVI", "MOV", "MKV", "FLV", "WMV", "WEBM", "MPEG", "MPG" <br />
Video: "MP4", "AVI", "MOV", "MKV", "FLV", "WMV", "WEBM", "MPEG", "MPG" (The video converter also support audio to video) <br />
Audio to Video: "MP3", "WAV", "AAC", "M4A", "OGG", "WMA", "FLAC" <br/ >

# How to build, run and export as exe
Use Visual Studio Code, install python and type this command to install library. <br/>
```bash
pip install pydub Pillow pillow-heif PyInstaller.
```
Download the source code and [FFmpeg for Windows](https://github.com/BtbN/FFmpeg-Builds/releases). <br/>
Choose ffmpeg-master-latest-win64-gpl.zip and extract ffmpeg.exe and place it in your file directory. <br/>
The file directory should be like this. <br/>
```bash
your_project/
├── main_app.py
├── audio_converter.py
├── image_converter.py
├── video_converter.py
├── convert-icon.ico
├── ffmpeg.exe (Windows only)
└── build.py
```
Than run the program in Visual Studio Code or export as exe file with using following command. <br/>
```bash
python build.py
```
After building, your EXE will be at: dist/FileConverter.exe <br/>

# !!Important!!
In the video converter, not sugget convert with "WEBM" which use a lot of CPU usage and slow

# Develop path
1. Image converter (done)
2. Audio converter (done)
3. Video to Audio converter (done)
4. Video conveter (done)
5. Audio to Video converter (done)
6. Document conveter (not yet)

# More function comming soon

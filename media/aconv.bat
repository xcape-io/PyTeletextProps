for %%f in (*.mp3) do (

  ffmpeg.exe -i %%~nf.mp3 -y %%~nf.wav
)
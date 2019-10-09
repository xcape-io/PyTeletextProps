C:\"Program Files"\7-Zip\7z.exe a -ttar teletextprops-%date:~6,4%%date:~3,2%%date:~0,2%.tar -xr!.git -xr!ready -xr!_SYNCAPP -xr!*.tgz -xr!*.vs -xr!*.pyc -xr!*.log.* -xr!.eric* -xr!_eric* -xr!__* ./
;C:\"Program Files"\7-Zip\7z.exe a -tgzip teletextprops-1.0-%date:~6,4%%date:~3,2%%date:~0,2%.tgz teletextprops-%date:~6,4%%date:~3,2%%date:~0,2%.tar
;del teletextprops-%date:~6,4%%date:~3,2%%date:~0,2%.tar

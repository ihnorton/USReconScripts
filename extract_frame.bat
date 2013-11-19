@ECHO OFF

REM Extract single slice

REM Requires PLUS in %PATH%
REM Arguments:
REM     frame
REM     file.mha

set /a frame1=%1
set /a frame2=%1+1

EditSeqMetaFile.exe ^
    --operation=TRIM ^
    --first-frame-index=%frame1% ^
    --last-frame-index=%frame2% ^
    --output-seq-file=C:\temp\us_frame.mha ^
    --source-seq-file=%2 

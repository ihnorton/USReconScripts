@ECHO OFF

REM Anonymize 1920x1080 BK ultrasound acquisition.

REM Requires PLUS build bin directory in %PATH%
REM Arguments:
REM     file.mha

EditSeqMetaFile.exe ^
    --operation=FILL_IMAGE_RECTANGLE ^
    --rect-origin 550 0 ^
    --rect-size 590 60 ^
    --source-seq-file=%1 ^
    --output-seq-file="%cd%"/"%~n1"_anon.mha

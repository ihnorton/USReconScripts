@ECHO OFF

REM Set path

REM set PATH=%PATH%;C:\neurosurgery\dev\PlusExperimental-bin-release\bin\Release\

REM Args:
REM     config_file.xml
REM     img_file.mha

VolumeReconstructor --config-file=%1 ^
    --img-seq-file=%2 ^
    --output-volume-file=output.mha ^
    --transform=ImageToTracker
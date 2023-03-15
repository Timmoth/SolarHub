$circuitPyDriveLetter = $(Get-Volume -FileSystemLabel 'CIRCUITPY').DriveLetter;
$circuitPyDrivePath = "${circuitPyDriveLetter}:/";
echo $circuitPyDrivePath
copy *.py $circuitPyDrivePath
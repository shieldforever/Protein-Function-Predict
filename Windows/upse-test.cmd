@echo off
echo "UltraPse Windows Auto Test"
echo "Classic PseAAC"
upse -i test\tiny.fas -u tdfs\classic-pseaac.lua -t 1 -l 10 -w 0.05 -f svm
pause
echo "Standard PseDNC"
upse -i test\tiny-dna.fas -u tdfs\psednc.lua -t 1 -l 3 -w 0.5 -f svm
pause
echo "OneHot Scheme"
upse -i test\tiny-one-hot-protein.fas -n stdprot -m user,OneHot.dll,ONEHOT -l 19 -f svm
pause
echo "User-define sequence type for PseAAC: 21 types of amino acids"
upse -i test\user-type.fas -u tdfs\user-type.lua -m pse -t 1 -l 10 -w 0.05 -f svm
pause
echo "User-define sequence type for AAC: 21 types of amino acids"
upse -i test\user-type.fas -u tdfs\user-type.lua -m comp -t 1 -l 10 -w 0.05 -f svm


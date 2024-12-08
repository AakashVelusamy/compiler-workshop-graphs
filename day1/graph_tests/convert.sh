for f in $(ls *.json);
do
  bril2txt < $f &> $f.ir
done
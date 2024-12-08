for f in $(ls *.json);
do
  echo $f
  python3 /home/pradeepku/bril/examples/cfg_dot.py < $f &> $f.out
done
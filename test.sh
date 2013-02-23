#! /bin/sh

for i in {1..30} ; do 
  HASH=$(./randomhash.py)
  echo -n $HASH
  echo -n " "
  RESULT=$(./invert.py hfile $HASH | cksum | awk '{ print $1 }')
  echo $RESULT
  if [ "$HASH" -ne "$RESULT" ]; then
    echo "FAILED"
    exit 1
  fi
done

echo "OK; 30 random tests passed."

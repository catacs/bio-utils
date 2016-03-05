#!/bin/bash
directory="$1/*"
outlaiers="./outliers.py"
extract="./extract_cols.py"
DATE=$(date +%m-%d-%Y)
for d in $directory;
do
  if [ -d "$d" ]; then
    outpath="$d/csv/$DATE"
    for file in $d/*.txt;
    do
      filename=$(basename "$file" ".txt")
      mkdir -p "$outpath"
      $outlaiers -i "$file" -o "$outpath/$filename.csv"
    done
    $extract -d "$outpath"
  fi
done

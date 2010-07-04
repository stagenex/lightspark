#!/bin/sh

if [ -d ../as3 ] && [ "$1" != "--override" ]; then
  echo "It seems you've already run this script. Please use --override to start again"
fi

mkdir -p ../downloaded_doc
mkdir -p ../as3
cd ../downloaded_doc
if [ ! -f help.adobe.com/en_US/AS3LCR/Flash_10.0/all-classes.html ]; then
  wget -r -k -l 1 http://help.adobe.com/en_US/AS3LCR/Flash_10.0/all-classes.html
fi

cp ../scripts/*.py help.adobe.com/en_US/AS3LCR/Flash_10.0
cd help.adobe.com/en_US/AS3LCR/Flash_10.0

find -name "*.html" -exec python runner.py "{}" ../../../../../as3 \;

# Apply patches here
cd ../../../../../scripts 
for file in ./doc_patchs/*
do
   echo "Applying patch $file"
   cat "$file" > patch -p 1 
done
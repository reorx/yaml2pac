#!/bin/bash

function nsrequest() {
    ./nsrequest/DerivedData/nsrequest/Build/Products/Release/nsrequest $1
}

tempfile=$(mktemp -t rules.pac)
yaml2pac data/rules.yaml > $tempfile
echo "File path: $tempfile"
yaml2pac data/rules.yaml -t $tempfile





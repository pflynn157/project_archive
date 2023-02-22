#!/bin/bash

test_count=0
TLC="build/src/tlc"

function gen_single_test() {
    name=`basename $1 .tl`
    base_path=`dirname $1`
    
    if [ ! -d $base_path/out ] ; then
        mkdir -p $base_path/out
    fi
    
    $TLC $1 -o $name
    ./$name > $base_path/out/$name.out
    echo $? > $base_path/out/$name.code
    
    rm ./$name
    rm /tmp/$name.o
    rm /tmp/$name.asm
    
    test_count=$((test_count+1))
}

function gen_test() {
    if [ ! -d $1/out ] ; then
	    mkdir -p $1/out
	else
	    rm $1/out/*
	fi
	
    for entry in $1/*.tl
    do
    	name=`basename $entry .tl`
    	
    	$TLC $entry -o $name
    	./$name > $1/out/$name.out
    	echo $? > $1/out/$name.code
    	
    	rm ./$name
    	rm /tmp/$name.o
    	rm /tmp/$name.asm
    	
    	test_count=$((test_count+1))
    done
}

flags=""

echo ""
echo "WARNING"
echo "This script assumes all test cases AND the current compiler build is correct."
echo "DO NOT RUN unless you are sure both cases are true."
echo ""

echo "Generating all tests..."
echo ""

if [[ $# == 1 ]] ; then
    gen_single_test $1
else
    gen_test 'test/basic'
    gen_test 'test/syntax'
    gen_test 'test/cond'
    gen_test 'test/loop'
    gen_test 'test/array'
    gen_test 'test/func'
    gen_test 'test/str'
    gen_test 'test/struct'
fi

echo ""
echo "$test_count generated successfully."
echo "Done"


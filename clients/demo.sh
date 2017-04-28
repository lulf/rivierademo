#!/bin/sh
./oc_freceive anycast &
./oc_freceive anycast &

./oc_freceive queue1 &
./oc_freceive queue1 &
./oc_freceive queue1 &

./oc_rsend anycast &
./oc_rsend anycast &
./oc_rsend queue1 &

wait

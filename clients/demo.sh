#!/bin/sh
/oc_freceive anycast &
/oc_freceive queue1 &
/oc_freceive queue1 &
sleep 20
/oc_rsend anycast $ADDRESS &
/oc_rsend queue1 $ADDRESS

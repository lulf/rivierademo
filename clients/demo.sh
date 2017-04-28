#!/bin/sh
WAIT_TIME=${1:-600}
/oc_freceive anycast &
/oc_freceive anycast &

/oc_freceive queue1 &
/oc_freceive queue1 &
/oc_freceive queue1 &

/oc_rsend anycast &
/oc_rsend anycast &
/oc_rsend queue1 &

sleep $WAIT_TIME

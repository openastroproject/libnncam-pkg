#!/bin/bash

version=`cat version`

rm -fr libmallincam-$version
rm -fr libmallincam_*
rm -fr libmallincam-dev_*
rm -f debfiles/compat
rm -f debfiles/patches/*

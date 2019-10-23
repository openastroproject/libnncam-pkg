#!/bin/bash

version=`cat version`

rm -fr libnncam-$version
rm -fr libnncam_*
rm -fr libnncam-dev_*
rm -f debfiles/compat
rm -f debfiles/patches/*

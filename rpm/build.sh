#!/bin/bash

rm -f libnncam-*.tar.gz
ln ../libnncam-*.tar.gz .
rel=`cut -d' ' -f3 < /etc/redhat-release`
fedpkg --release f$rel local

#!/bin/bash

export DEBEMAIL=james@openastroproject.org
export DEBFULLNAME="James Fidell"

version=`cat version`

srcdir=libnncam-$version
debdir=debian
debsrc=$debdir/source
quiltconf=$HOME/.quiltrc-dpkg

debversion=`cat /etc/debian_version`
case $debversion in
	jessie/sid)
		compatversion=9
		;;
	stretch/sid)
		compatversion=9
		;;
	*)
		compatversion=10
		;;
esac
echo $compatversion > debfiles/compat

mkdir -p debfiles/patches
cp ../patches/*.patch debfiles/patches

tar zxf ../libnncam-$version.tar.gz
cd $srcdir
test -d demo && ( chmod -x demo/*.* Makefile )
YFLAG=-y
dh_make -v | fgrep -q '1998-2011'
if [ $? -eq 0 ]
then
  YFLAG=''
fi
dh_make $YFLAG -l -f ../../libnncam-$version.tar.gz

sed -e "s/@@COMPAT@@/$compatversion/" < ../debfiles/control > $debdir/control
cp ../debfiles/copyright $debdir
cp ../debfiles/changelog $debdir
cp ../debfiles/compat $debdir
cp ../debfiles/watch $debdir
cp ../debfiles/libnncam.dirs $debdir
cp ../debfiles/libnncam.install $debdir
cp ../debfiles/libnncam.symbols $debdir
cp ../debfiles/libnncam.triggers $debdir
cp ../debfiles/libnncam-dev.dirs $debdir
cp ../debfiles/libnncam-dev.install $debdir

echo 10 > $debdir/compat

sed -e '/^.*[ |]configure./a\
	udevadm control --reload-rules || true' < $debdir/postinst.ex > $debdir/postinst
chmod +x $debdir/postinst
sed -e '/^.*[ |]remove./a\
	udevadm control --reload-rules || true' < $debdir/postrm.ex > $debdir/postrm
chmod +x $debdir/postrm
echo "3.0 (quilt)" > $debsrc/format

sed -e "s/DEBVERSION/$version/g" < ../debfiles/rules.overrides >> $debdir/rules

rm $debdir/README.Debian
rm $debdir/README.source
rm -f $debdir/libnncam-docs.docs
rm $debdir/libnncam1.*
rm $debdir/*.[Ee][Xx]


export QUILT_PATCHES="debian/patches"
export QUILT_PATCH_OPTS="--reject-format=unified"
export QUILT_DIFF_ARGS="-p ab --no-timestamps --no-index --color=auto"
export QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"
mkdir -p $QUILT_PATCHES

for p in `ls -1 ../debfiles/patches`
do
  quilt --quiltrc=$quiltconf new $p
  for f in `egrep '^\+\+\+' ../debfiles/patches/$p | awk '{ print $2; }'`
  do
    quilt --quiltrc=$quiltconf add $f
  done
pwd
  patch -p0 < ../debfiles/patches/$p
  quilt --quiltrc=$quiltconf refresh
done

dpkg-buildpackage -us -uc

echo "Now run:"
echo
echo "    lintian -i -I --show-overrides libnncam_$version-1_amd64.changes"

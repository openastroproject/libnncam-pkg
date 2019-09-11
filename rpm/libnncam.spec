%define debug_package %{nil}

Name:           libnncam
Version:        1.37.14643
Release:        0
Summary:        Risingcam and Levenhuk camera support library
License:	GPLv2+
Prefix:         %{_prefix}
Provides:       libnncam = %{version}-%{release}
Obsoletes:      libnncam < 1.37.14643
Source:         libnncam-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libnncam is a user-space driver for Risingcam and Levenhuk astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libnncam-devel = %{version}-%{release}
Obsoletes:      libnncam-devel < 1.37.14643

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libnncam.pc.in > libnncam.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}/etc/udev/rules.d
mkdir -p %{buildroot}%{_includedir}

case %{_arch} in
  x86_64)
    cp x64/libnncam.bin %{buildroot}%{_libdir}/libnncam.so.%{version}
		cp nncam.h %{buildroot}%{_includedir}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp 70-risingcam-cameras.rules %{buildroot}/etc/udev/rules.d

%post
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%files
%{_libdir}/*.so.*
%{_sysconfdir}/udev/rules.d/*.rules

%files devel
%{_includedir}/nncam.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Sep 11 2019 James Fidell <james@openastroproject.org> - 1.37.14643
- Initial RPM release


%define debug_package %{nil}

Name:           libmallincam
Version:        1.48.18332
Release:        0
Summary:        Mallincam camera support library
License:	GPLv2+
Prefix:         %{_prefix}
Provides:       libmallincam = %{version}-%{release}
Obsoletes:      libmallincam < 1.48.18332
Source:         libmallincam-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libmallincam is a user-space driver for Mallincam astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libmallincam-devel = %{version}-%{release}
Obsoletes:      libmallincam-devel < 1.48.18332

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libmallincam.pc.in > libmallincam.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}/etc/udev/rules.d
mkdir -p %{buildroot}%{_includedir}

case %{_arch} in
  x86_64)
    cp linux/x64/libmallincam.so %{buildroot}%{_libdir}/libmallincam.so.%{version}
		cp inc/mallincam.h %{buildroot}%{_includedir}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp 70-mallincam-cameras.rules %{buildroot}/etc/udev/rules.d

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
%{_includedir}/mallincam.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Apr 28 2021 James Fidell <james@openastroproject.org> - 1.48.18332-0
- Initial RPM release


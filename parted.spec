%define _disable_ld_no_undefined 1

%define	major	2
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%define	fsresize_major	0
%define	libfsresize	%mklibname %{name}-fs-resize %{fsresize_major}

%bcond_without	uclibc

Summary:	Flexible partitioning tool
Name:		parted
Version:	3.2
Release:	4
License:	GPLv3+
Group:		System/Configuration/Hardware
Url:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
Source1:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz.sig
Patch0:		parted-3.2-parted-fs-resize-uuid-linkage.patch
Patch1:		udevadm-settle.patch

BuildRequires:	gettext-devel >= 0.18
BuildRequires:	gpm-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(uuid)
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-9
BuildRequires:	uclibc-readline-devel
BuildRequires:	uclibc-libdevmapper-devel
BuildRequires:	uclibc-ext2fs-devel
BuildRequires:	uclibc-ncurses-devel
BuildRequires:	uclibc-libuuid-devel
%endif

%description
GNU Parted is a program that allows you to create, destroy,
resize, move and copy hard disk partitions. This is useful for
creating space for new operating systems, reorganising disk
usage, and copying data to new hard disks.

%package -n	%{libname}
Summary:	The parted library
Group:		Development/C

%description -n %{libname}
This package includes the dynamic libraries

%package -n	%{libfsresize}
Summary:	The parted fs-resize library
Group:		Development/C

%description -n %{libfsresize}
This package includes the dynamic libraries



%if %{with uclibc}
%package -n	uclibc-%{name}
Summary:	Flexible partitioning tool
Group:		System/Configuration/Hardware

%description -n	uclibc-%{name}
GNU Parted is a program that allows you to create, destroy,
resize, move and copy hard disk partitions. This is useful for
creating space for new operating systems, reorganising disk
usage, and copying data to new hard disks.

%package -n	uclibc-%{libname}
Summary:	The parted library (uClibc linked) (uClibc linked)
Group:		Development/C

%description -n uclibc-%{libname}
This package includes the dynamic libraries

%package -n	uclibc-%{libfsresize}
Summary:	The parted fs-resize library (uClibc linked)
Group:		Development/C

%description -n uclibc-%{libfsresize}
This package includes the dynamic libraries

%package -n	uclibc-%{devname}
Summary:	Files required to compile software that uses lib%{name}
Group:		Development/C
Requires:	uclibc-%{libname} = %{EVRD}
Requires:	uclibc-%{libfsresize} = %{EVRD}
Requires:	%{devname} = %{EVRD}
Provides:	uclibc-parted-devel = %{EVRD}
Provides:	uclibc-libparted-devel = %{EVRD}
Conflicts:	%{devname} < 3.2-4

%description -n uclibc-%{devname}
This package includes the header files and libraries needed to
link software with lib%{name}.
%endif

%package -n	%{devname}
Summary:	Files required to compile software that uses lib%{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libfsresize} = %{EVRD}
Provides:	parted-devel = %{EVRD}

%description -n %{devname}
This package includes the header files and libraries needed to
link software with lib%{name}.

%prep
%setup -q
%apply_patches

%build
CONFIGURE_TOP="$PWD"

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--enable-device-mapper \
	--with-readline \
	--enable-static \
	--with-pic \
	--disable-assert
%make V=1 CC=%{uclibc_cc} CFLAGS="%{uclibc_cflags}"
popd
%endif

mkdir -p system
pushd system
%configure \
	--enable-device-mapper \
	--enable-static \
	--with-readline \
	--with-pic
%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
%endif

%makeinstall_std -C system

%find_lang %{name}

%check
# check fails due to /dev not mounted in chroot on bs..
make -C system check || /bin/true

%files -f %{name}.lang
%doc README
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_mandir}/man8/parted.8*
%{_mandir}/man8/partprobe.8*
%{_infodir}/parted.info*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_sbindir}/parted
%{uclibc_root}%{_sbindir}/partprobe
%endif

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/lib%{name}.so.%{major}*
%endif

%files -n %{libfsresize}
%{_libdir}/lib%{name}-fs-resize.so.%{fsresize_major}*

%if %{with uclibc}
%files -n uclibc-%{libfsresize}
%{uclibc_root}%{_libdir}/lib%{name}-fs-resize.so.%{fsresize_major}*

%files -n uclibc-%{devname}
%{uclibc_root}%{_libdir}/lib%{name}.a
%{uclibc_root}%{_libdir}/lib%{name}.so
%{uclibc_root}%{_libdir}/lib%{name}-fs-resize.a
%{uclibc_root}%{_libdir}/lib%{name}-fs-resize.so
%endif

%files -n %{devname}
%doc AUTHORS ChangeLog doc/API TODO
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-fs-resize.a
%{_libdir}/lib%{name}-fs-resize.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/lib%{name}.pc


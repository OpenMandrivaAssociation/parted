%define _disable_ld_no_undefined 1

%define	major		2
%define	libname		%mklibname %{name} %{major}
%define	devname		%mklibname %{name} -d

%define	fsresize_major	0
%define	libfsresize	%mklibname %{name}-fs-resize %{fsresize_major}

%bcond_without	uclibc

Name:		parted
Version:	3.1
Release:	3
Summary:	Flexible partitioning tool
License:	GPLv3+
Group:		System/Configuration/Hardware
URL:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.xz
Source1:	http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.xz.sig
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	gettext-devel >= 0.18
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
Requires:	e2fsprogs

%package -n	uclibc-%{name}
Summary:	Flexible partitioning tool
Group:		System/Configuration/Hardware

%package -n	%{libname}
Summary:	The parted library
Group:		Development/C
Obsoletes:	%{mklibname %{name} 1.7} = %{version}

%package -n	uclibc-%{libname}
Summary:	The parted library (uClibc linked) (uClibc linked)
Group:		Development/C

%package -n	%{libfsresize}
Summary:	The parted fs-resize library
Group:		Development/C

%package -n	uclibc-%{libfsresize}
Summary:	The parted fs-resize library (uClibc linked)
Group:		Development/C

%package -n	%{devname}
Summary:	Files required to compile software that uses libparted
Group:		Development/C
Requires:	e2fsprogs
Requires:	%{libname} = %{version}
Requires:	%{libfsresize} = %{version}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
Requires:	uclibc-%{libfsresize} = %{EVRD}
%endif
Provides:	parted-devel = %{version}
Obsoletes:	%{mklibname -d parted 1.8 7} < %{version}
Obsoletes:	%{mklibname -d parted 1.8 8} < %{version}-%{release}
Obsoletes:	%{mklibname -d parted 1.8 2} < %{version}
Obsoletes:	%{mklibname -d parted 1.8 1} < %{version}
Obsoletes:	%{mklibname -d parted 1.7 1} < %{version}

%description
GNU Parted is a program that allows you to create, destroy,
resize, move and copy hard disk partitions. This is useful for
creating space for new operating systems, reorganising disk
usage, and copying data to new hard disks.

%description -n	uclibc-%{name}
GNU Parted is a program that allows you to create, destroy,
resize, move and copy hard disk partitions. This is useful for
creating space for new operating systems, reorganising disk
usage, and copying data to new hard disks.

%description -n %{libname}
This package includes the dynamic libraries

%description -n uclibc-%{libname}
This package includes the dynamic libraries

%description -n %{libfsresize}
This package includes the dynamic libraries

%description -n uclibc-%{libfsresize}
This package includes the dynamic libraries

%description -n %{devname}
This package includes the header files and libraries needed to
link software with libparted.

%prep
%setup -q
autoreconf -fi

%build
export CONFIGURE_TOP=$PWD

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%configure2_5x	CC=%{uclibc_cc} \
		CFLAGS="%{uclibc_cflags}" \
		--libdir=%{uclibc_root}%{_libdir} \
		--sbindir=%{uclibc_root}%{_sbindir} \
		--enable-device-mapper \
		--without-readline \
		--with-pic \
		--disable-assert
%make V=1 CC=%{uclibc_cc} CFLAGS="%{uclibc_cflags}"
popd
%endif

mkdir -p system
pushd system
%configure2_5x	--enable-device-mapper \
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
make -C system check

%files -f %{name}.lang
%doc README
%{_sbindir}/*
%{_mandir}/man*/*
%{_infodir}/parted.info*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_sbindir}/parted
%{uclibc_root}%{_sbindir}/partprobe
%endif

%files -n %{libname}
%doc TODO
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
%endif

%files -n %{devname}
%doc AUTHORS ChangeLog doc/API
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/lib*.a
%{uclibc_root}%{_libdir}/lib*.so
%endif
%{_includedir}/*
%{_libdir}/pkgconfig/libparted.pc

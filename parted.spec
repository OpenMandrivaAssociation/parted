%define Werror_cflags %nil
%define	major 	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

Name:		parted
Version:	3.0
Release:	3
Summary:	Flexible partitioning tool
License:	GPLv3+
Group:		System/Configuration/Hardware
URL:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.xz
Source1:	http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.xz.sig
Requires(post):	info-install
Requires(preun):info-install
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
Requires:	e2fsprogs

%package -n	%{libname}
Summary:	The parted library
Group:		Development/C
Obsoletes:	%{mklibname %{name} 1.7} = %{version}

%package -n	%{devname}
Summary:	Files required to compile software that uses libparted
Group:		Development/C
Requires:	e2fsprogs
Requires:	%{libname} = %{version}
Provides:	parted-devel = %{version}
Obsoletes:	%{mklibname -d parted 1.8 7} < %{version}
Obsoletes:	%{mklibname -d parted 1.8 8} < %{version}-%{release}
Obsoletes:	%{mklibname -d parted 1.8 2} < %{version}
Obsoletes:      %{mklibname -d parted 1.8 1} < %{version}
Obsoletes:	%{mklibname -d parted 1.7 1} < %{version}

%description
GNU Parted is a program that allows you to create, destroy,
resize, move and copy hard disk partitions. This is useful for
creating space for new operating systems, reorganising disk
usage, and copying data to new hard disks.

%description -n %{libname}
This package includes the dynamic libraries

%description -n %{devname}
This package includes the header files and libraries needed to
link software with libparted.

%prep
%setup -q
autoreconf -fi

%build
%configure2_5x	--enable-device-mapper \
		--with-readline \
		--with-pic
%make

%install
%makeinstall_std

%find_lang %{name}

%check
export PATH=$PATH:/sbin
make check

%post
%_install_info %{name}

%preun
%_remove_install_info %{name}

%files -f %{name}.lang
%doc README
%{_sbindir}/*
%{_mandir}/man*/*
%{_infodir}/parted.info*

%files -n %{libname}
%doc TODO
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog doc/API
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/libparted.pc

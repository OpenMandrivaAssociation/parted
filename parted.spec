%define name	parted
%define	version	1.8.6
%define release %mkrel 1
%define major   1.8
%define major_  6
%define libname %mklibname %{name}%{major}_ %{major_}

Summary:	Flexible partitioning tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Hardware
BuildRequires:	gpm-devel ncurses-devel e2fsprogs-devel
BuildRequires: 	automake1.8
URL:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.bz2

Patch100:	parted-1.8.6-disksunraid.patch
# libreadline.so should refer libncurses.so since it needs it,
# but we don't want this for bootstrapping issue (?)
# so removing as-needed when detecting libreadline.so otherwise it fails
Patch101:	parted-1.8.6-fix-readline-detection-in-configure.patch

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	e2fsprogs-devel readline-devel device-mapper-devel gettext-devel libreadline-devel

%package -n	%{libname}
Summary:	Files required to compile software that uses libparted
Group:		Development/C
Requires:	e2fsprogs
Obsoletes: %{mklibname %name 1.7} = %version

%package -n	%{libname}-devel
Summary:	Files required to compile software that uses libparted
Group:		Development/C
Requires:	e2fsprogs %{libname} = %{version}
Provides:       libparted-devel libparted%{major}-devel parted-devel
Obsoletes:      parted-devel
Conflicts:     	libparted1.7_1-devel
Conflicts:     	libparted1.8_1-devel
Conflicts:     	libparted1.8_2-devel

%description
GNU Parted is a program that allows you to create, destroy,
resize, move and copy hard disk partitions. This is useful for
creating space for new operating systems, reorganising disk
usage, and copying data to new hard disks.

%description -n	%{libname}
This package includes the dynamic libraries

%description -n	%{libname}-devel
This package includes the header files and libraries needed to
link software with libparted.

%prep
%setup -q

%patch100 -p1 -b .disksunraid
%patch101 -p1

%build
autoconf
%configure2_5x --disable-Werror --enable-device-mapper

%make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}

# test program, it should not be installed, but it happens, i don't know why
rm -f $RPM_BUILD_ROOT/usr/bin/label

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}

%preun
%_remove_install_info %{name}

%post   -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,755)
%doc README
%{_sbindir}/*
%{_mandir}/man*/*
%{_infodir}/parted.info*

%files -n %{libname}
%defattr(-,root,root,755)
%doc TODO
%{_libdir}/lib%{name}-%{major}.so.%{major_}*

%files -n %{libname}-devel
%defattr(-,root,root,755)
%doc AUTHORS ChangeLog doc/API
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/libparted.pc

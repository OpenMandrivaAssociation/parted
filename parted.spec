%define major   1.8
%define major_  8
%define libname %mklibname %{name}%{major}_ %{major_}
%define develname %mklibname %{name} -d

Name:           parted
Version:        1.8.8
Release:        %mkrel 5
Summary:        Flexible partitioning tool
License:        GPLv3+
Group:          System/Configuration/Hardware
URL:            http://www.gnu.org/software/parted/
Source0:        http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.bz2
Source1:        http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.bz2.sha1
Source2:        http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.bz2.sha1.sig
Source3:        http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.bz2.sig
Patch0:         parted-1.8.6-disksunraid.patch
# libreadline.so should refer libncurses.so since it needs it,
# but we don't want this for bootstrapping issue (?)
# so removing as-needed when detecting libreadline.so otherwise it fails
Patch1:         parted-1.8.8-fix-readline-detection-in-configure.patch
Patch2:		gnulib.diff
Requires(post): info-install
Requires(preun):info-install
BuildRequires:  device-mapper-devel
BuildRequires:  gettext-devel
BuildRequires:  libe2fsprogs-devel
BuildRequires:  libgpm-devel
BuildRequires:  libncurses-devel
BuildRequires:  libreadline-devel
BuildConflicts: check-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%package -n %{libname}
Summary:        Files required to compile software that uses libparted
Group:          Development/C
Requires:       e2fsprogs
Obsoletes:      %{mklibname %{name} 1.7} = %{version}

%package -n %{develname}
Summary:        Files required to compile software that uses libparted
Group:          Development/C
Requires:       e2fsprogs
Requires:       %{libname} = %{version}
Provides:       libparted-devel = %{version}
Provides:       libparted%{major}-devel = %{version}
Provides:       parted-devel = %{version}
Provides:       %{_lib}parted%{major}-devel = %{version}
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

%description -n %{develname}
This package includes the header files and libraries needed to
link software with libparted.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0

%build
libtoolize --install --force
%configure2_5x --disable-Werror --enable-device-mapper
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%post
%_install_info %{name}

%preun
%_remove_install_info %{name}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc README
%{_sbindir}/*
%{_mandir}/man*/*
%{_infodir}/parted.info*

%files -n %{libname}
%defattr(-,root,root,0755)
%doc TODO
%{_libdir}/lib%{name}-%{major}.so.%{major_}*

%files -n %{develname}
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog doc/API
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/libparted.pc

%define major   1.8
%define major_  7
%define libname %mklibname %{name}%{major}_ %{major_}

Name:           parted
Version:        1.8.7
Release:        %mkrel 1
Summary:        Flexible partitioning tool
License:        GPL
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
Patch1:         parted-1.8.6-fix-readline-detection-in-configure.patch
Requires(post): info-install
Requires(preun):info-install
BuildRequires:  device-mapper-devel
BuildRequires:  gettext-devel
BuildRequires:  libe2fsprogs-devel
BuildRequires:  libgpm-devel
BuildRequires:  libncurses-devel
BuildRequires:  libreadline-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%package -n %{libname}
Summary:        Files required to compile software that uses libparted
Group:          Development/C
Requires:       e2fsprogs
Obsoletes:      %{mklibname %{name} 1.7} = %{version}

%package -n %{libname}-devel
Summary:        Files required to compile software that uses libparted
Group:          Development/C
Requires:       e2fsprogs
Requires:       %{libname} = %{version}
Provides:       libparted-devel = %{version}
Provides:       libparted%{major}-devel = %{version}
Provides:       parted-devel = %{version}
Provides:       %{_lib}parted%{major}-devel = %{version}
Obsoletes:      parted-devel < %{version}
Conflicts:      libparted1.7_1-devel
Conflicts:      libparted1.8_1-devel
Conflicts:      libparted1.8_2-devel

%description
GNU Parted is a program that allows you to create, destroy,
resize, move and copy hard disk partitions. This is useful for
creating space for new operating systems, reorganising disk
usage, and copying data to new hard disks.

%description -n %{libname}
This package includes the dynamic libraries

%description -n %{libname}-devel
This package includes the header files and libraries needed to
link software with libparted.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{_bindir}/autoconf
%{configure2_5x} --disable-Werror --enable-device-mapper
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall}

%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%post
%_install_info %{name}

%preun
%_remove_install_info %{name}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(0644,root,root,0755)
%doc README
%attr(0755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
%{_infodir}/parted.info*

%files -n %{libname}
%defattr(0644,root,root,0755)
%doc TODO
%attr(0755,root,root) %{_libdir}/lib%{name}-%{major}.so.%{major_}*

%files -n %{libname}-devel
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog doc/API
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/libparted.pc

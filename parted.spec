%define Werror_cflags %nil
%define major  0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:           parted
Version:        2.3
Release:        %mkrel 4
Summary:        Flexible partitioning tool
License:        GPLv3+
Group:          System/Configuration/Hardware
URL:            http://www.gnu.org/software/parted/
Source0:        http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.xz
Source1:        http://ftp.gnu.org/gnu/parted/parted-%{version}.tar.xz.sig
# upstream commit 244b1b25a12198efb076e8c65be77b5750776583
Patch0:		parted-2.3-assert.patch
Patch1:		parted-2.3-assert2.patch
Requires(post): info-install
Requires(preun):info-install
BuildRequires:  device-mapper-devel
BuildRequires:  gettext-devel
BuildRequires:  libe2fsprogs-devel
BuildRequires:  libuuid-devel
BuildRequires:  libgpm-devel
BuildRequires:  libncurses-devel
BuildRequires:  libreadline-devel
BuildRequires:	util-linux
BuildConflicts: check-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%package -n %{libname}
Summary:        The parted library
Group:          Development/C
Requires:       e2fsprogs
Obsoletes:      %{mklibname %{name} 1.7} = %{version}

%package -n %{develname}
Summary:        Files required to compile software that uses libparted
Group:          Development/C
Requires:       e2fsprogs
Requires:       %{libname} = %{version}
Provides:       libparted-devel = %{version}
Provides:       libparted%{api}-devel = %{version}
Provides:       parted-devel = %{version}
Provides:       %{_lib}parted%{api}-devel = %{version}
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

%build
%configure2_5x	--disable-Werror \
		--enable-device-mapper \
		--with-readline \
		--with-pic
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

%check
export PATH=$PATH:/sbin
make check

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
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog doc/API
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/libparted.pc

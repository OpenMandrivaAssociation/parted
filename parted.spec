%define _disable_ld_no_undefined 1

%define	major	2
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%define	fsresize_major	0
%define	libfsresize	%mklibname %{name}-fs-resize %{fsresize_major}

%bcond_without	uclibc

Summary:	Flexible partitioning tool
Name:		parted
Version:	3.1
Release:	8
License:	GPLv3+
Group:		System/Configuration/Hardware
Url:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
Source1:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz.sig

Patch0:		parted-3.0-libparted-copy-pmbr_boot-when-duplicating-GPT-disk.patch
Patch1:		parted-3.1-libparted-check-PMBR-before-GPT-partition-table-8052.patch
Patch2:		parted-3.1-tests-add-t0301-overwrite-gpt-pmbr.sh.patch
Patch3:		parted-3.1-libparted-Fix-endian-error-with-FirstUsableLBA.patch
Patch4:		parted-2.1-libparted-use-dm_udev_wait-698121.patch
Patch5:		parted-3.1-libparted-use-largest_partnum-in-dm_reread_part_tabl.patch
patch6:		parted-3.1-test-creating-20-device-mapper-partitions.patch
Patch7:		parted-3.1-libparted-preserve-the-uuid-on-dm-partitions.patch
Patch8:		parted-3.1-tests-Make-sure-dm-UUIDs-are-not-erased.patch
Patch9:		parted-3.1-libparted-reallocate-buf-after-_disk_analyse_block_s.patch
Patch10:	parted-3.1-tests-cleanup-losetup-usage.patch
Patch11:	parted-3.1-libparted-add-support-for-implicit-FBA-DASD-partitions.patch
Patch12:	parted-3.1-libparted-add-support-for-EAV-DASD-partitions.patch

BuildRequires:	gettext-devel >= 0.18
BuildRequires:	gpm-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(uuid)

%package -n	uclibc-%{name}
Summary:	Flexible partitioning tool
Group:		System/Configuration/Hardware

%package -n	%{libname}
Summary:	The parted library
Group:		Development/C

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
Summary:	Files required to compile software that uses lib%{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libfsresize} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
Requires:	uclibc-%{libfsresize} = %{EVRD}
%endif
Provides:	parted-devel = %{EVRD}

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
link software with lib%{name}.

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
CONFIGURE_TOP="$PWD"

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--enable-device-mapper \
	--with-readline \
	--with-pic \
	--disable-assert
%make V=1 CC=%{uclibc_cc} CFLAGS="%{uclibc_cflags}"
popd
%endif

mkdir -p system
pushd system
%configure2_5x \
	--enable-device-mapper \
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
%endif

%files -n %{devname}
%doc AUTHORS ChangeLog doc/API TODO
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-fs-resize.a
%{_libdir}/lib%{name}-fs-resize.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/lib%{name}.a
%{uclibc_root}%{_libdir}/lib%{name}.so
%{uclibc_root}%{_libdir}/lib%{name}-fs-resize.a
%{uclibc_root}%{_libdir}/lib%{name}-fs-resize.so
%endif
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/lib%{name}.pc


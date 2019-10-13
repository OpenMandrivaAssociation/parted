%define _disable_ld_no_undefined 1

%define major 2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define fsresize_major 0
%define libfsresize %mklibname %{name}-fs-resize %{fsresize_major}

Summary:	Flexible partitioning tool
Name:		parted
Version:	3.3
Release:	1
License:	GPLv3+
Group:		System/Configuration/Hardware
Url:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
Patch0:		parted-3.2-parted-fs-resize-uuid-linkage.patch

# (tpg) patches from SuSE
Patch501:	parted-2.4-ncursesw6.patch
Patch502:	libparted-avoid-libdevice-mapper-warnings.patch
Patch503:	libparted-open-the-device-RO-and-lazily-switch-to-RW.patch
Patch504:	more-reliable-informing-the-kernel.patch

BuildRequires:	texinfo
BuildRequires:	gettext-devel >= 0.18
BuildRequires:	glibc-devel
BuildRequires:	pkgconfig(readline)
BuildRequires:	hostname
BuildRequires:	gperf
BuildRequires:	pkgconfig(devmapper) >= 1.02.153
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(blkid)

%description
GNU Parted is a program that allows you to create, destroy,
resize, move and copy hard disk partitions. This is useful for
creating space for new operating systems, reorganising disk
usage, and copying data to new hard disks.

%package -n %{libname}
Summary:	The parted library
Group:		Development/C

%description -n %{libname}
This package includes the dynamic libraries

%package -n %{libfsresize}
Summary:	The parted fs-resize library
Group:		Development/C

%description -n %{libfsresize}
This package includes the dynamic libraries

%package -n %{devname}
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
%autopatch -p1

%build
export CFLAGS="%{optflags} $(ncursesw6-config --cflags)"
export LIBS="$(ncursesw6-config --libs)"

%configure \
	--without-included-regex \
	--enable-device-mapper \
	--enable-static \
	--with-readline \
	--enable-threads=posix \
	--with-packager="%{vendor}" \
	--with-packager-bug-reports="%{bugurl}" \
	--with-pic

cat config.log

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

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

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{libfsresize}
%{_libdir}/lib%{name}-fs-resize.so.%{fsresize_major}*

%files -n %{devname}
%doc AUTHORS ChangeLog doc/API TODO
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-fs-resize.a
%{_libdir}/lib%{name}-fs-resize.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/lib%{name}*.pc

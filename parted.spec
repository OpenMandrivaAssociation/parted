%define _disable_ld_no_undefined 1

%define major 2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define fsresize_major 0
%define libfsresize %mklibname %{name}-fs-resize %{fsresize_major}

Summary:	Flexible partitioning tool
Name:		parted
Version:	3.2
Release:	7
License:	GPLv3+
Group:		System/Configuration/Hardware
Url:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
Patch0:		parted-3.2-parted-fs-resize-uuid-linkage.patch
Patch1:		udevadm-settle.patch
Patch2:		0001-tests-Try-several-UTF8-locales.patch
Patch3:		0002-maint-post-release-administrivia.patch
Patch4:		0003-libparted-also-link-to-UUID_LIBS.patch
Patch5:		0004-lib-fs-resize-Prevent-crash-resizing-FAT16-file-syst.patch
Patch6:		0005-tests-t3000-resize-fs.sh-Add-FAT16-resizing-test.patch
Patch7:		0006-tests-t3000-resize-fs.sh-Add-requirement-on-mkfs.vfa.patch
Patch8:		0007-tests-Change-minimum-size-to-256MiB.patch
Patch9:		0008-parted-don-t-crash-in-disk_set-when-disk-label-not-f.patch
Patch10:	0009-tests-Add-a-test-for-device-mapper-partition-sizes.patch
Patch11:	0010-libparted-device-mapper-uses-512b-sectors.patch
Patch12:	0011-Update-manpage-NAME-so-whatis-will-work.patch
Patch13:	0012-tests-Make-sure-the-extended-partition-length-is-cor.patch
Patch14:	0013-libparted-BLKPG_RESIZE_PARTITION-uses-bytes-not-sect.patch
Patch15:	0014-parted-Fix-crash-with-name-command-and-no-disklabel-.patch
Patch16:	0015-UI-Avoid-memory-leaks.patch
Patch17:	0016-libparted-Fix-memory-leaks.patch
Patch18:	0017-libparted-Fix-possible-memory-leaks.patch
Patch19:	0018-libparted-Stop-converting-.-in-sys-path-to.patch
Patch20:	0019-libparted-Use-read-only-when-probing-devices-on-linu.patch
Patch21:	0020-tests-Use-wait_for_dev_to_-functions.patch
Patch22:	0021-fdasd-geometry-handling-updated-from-upstream-s390-t.patch
Patch24:	0024-fdasd.c-Safeguard-against-geometry-misprobing.patch

BuildRequires:	gettext-devel >= 0.18
BuildRequires:	gpm-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(uuid)

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
%configure \
	--enable-device-mapper \
	--enable-static \
	--with-readline \
	--with-pic

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std

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
%{_libdir}/pkgconfig/lib%{name}.pc

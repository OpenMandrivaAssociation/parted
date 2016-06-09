%define _disable_ld_no_undefined 1

%define major 2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define fsresize_major 0
%define libfsresize %mklibname %{name}-fs-resize %{fsresize_major}

Summary:	Flexible partitioning tool
Name:		parted
Version:	3.2
Release:	8
License:	GPLv3+
Group:		System/Configuration/Hardware
Url:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
Patch0:		parted-3.2-parted-fs-resize-uuid-linkage.patch


# (tpg) patches from upstream git
Patch100:	0000-maint-post-release-administrivia.patch
Patch101:	0001-libparted-also-link-to-UUID_LIBS.patch
Patch102:	0002-lib-fs-resize-Prevent-crash-resizing-FAT16-file-syst.patch
Patch103:	0003-tests-t3000-resize-fs.sh-Add-FAT16-resizing-test.patch
Patch104:	0004-tests-t3000-resize-fs.sh-Add-requirement-on-mkfs.vfa.patch
Patch105:	0005-tests-Change-minimum-size-to-256MiB.patch
Patch106:	0006-parted-don-t-crash-in-disk_set-when-disk-label-not-f.patch
Patch107:	0007-tests-Add-a-test-for-device-mapper-partition-sizes.patch
Patch108:	0008-libparted-device-mapper-uses-512b-sectors.patch
Patch109:	0009-Update-manpage-NAME-so-whatis-will-work.patch
Patch110:	0010-libparted-arch-linux.c-Compile-without-ENABLE_DEVICE.patch
Patch111:	0011-libparted-fs-xfs-platform_defs.h-Include-fcntl.h-for.patch
Patch112:	0012-tests-Fall-back-to-C.UTF-8-if-no-en_US.utf8-availabl.patch
Patch113:	0013-doc-Fix-url-for-LWN-article.patch
Patch114:	0014-tests-Make-sure-the-extended-partition-length-is-cor.patch
Patch115:	0015-libparted-BLKPG_RESIZE_PARTITION-uses-bytes-not-sect.patch
Patch116:	0016-mac-copy-partition-type-and-name-correctly.patch
#Patch117:	0017-merge-HACKING-and-README-hacking.patch
#Patch118:	0018-Fwd-PATCH-2-2-add-verbose-test-documentation.patch
Patch119:	0019-parted-Fix-crash-with-name-command-and-no-disklabel-.patch
Patch120:	0020-UI-Avoid-memory-leaks.patch
Patch121:	0021-libparted-Fix-memory-leaks.patch
Patch122:	0022-libparted-Fix-possible-memory-leaks.patch
Patch123:	0023-libparted-Stop-converting-.-in-sys-path-to.patch
Patch124:	0024-libparted-Fix-misspelling-in-hfs-exception-string.patch
Patch125:	0025-libparted-Use-read-only-when-probing-devices-on-linu.patch
Patch126:	0026-tests-Use-wait_for_dev_to_-functions.patch
Patch127:	0027-fdasd-geometry-handling-updated-from-upstream-s390-t.patch
Patch128:	0028-dasd-enhance-device-probing.patch
Patch129:	0029-parted-fix-build-error-on-s390.patch
Patch130:	0030-fdasd.c-Safeguard-against-geometry-misprobing.patch
Patch131:	0031-lib-fs-resize-Prevent-crash-resizing-FAT-with-very-d.patch
Patch132:	0032-tests-t3000-resize-fs.sh-Add-very-deep-directory.patch
Patch133:	0033-Use-BLKSSZGET-to-get-device-sector-size-in-_device_p.patch
Patch134:	0034-parted-fix-the-rescue-command.patch
Patch135:	0035-Use-disk-geometry-as-basis-for-ext2-sector-sizes.patch
Patch136:	0036-Add-libparted-fs-resize.pc.patch
Patch137:	0037-docs-Add-list-of-filesystems-for-fs-type-1311596.patch
Patch138:	0038-parted-Display-details-of-partition-alignment-failur.patch
Patch139:	0039-lib-fs-resize-Fix-recognition-of-FAT-file-system-aft.patch
Patch140:	0040-bug-17883-PATCH-configure.ac-uclinux-is-also-linux.patch
Patch141:	0041-Add-NEWS-entry-for-fat-resize-fix.patch
Patch142:	0042-libparted-Remove-fdasd-geometry-code-from-alloc_meta.patch
Patch143:	0043-libparted-Fix-probing-AIX-disks-on-other-arches.patch

# (tpg) from debian, dunno it is usefull for anything
#Patch500:	udevadm-settle.patch

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

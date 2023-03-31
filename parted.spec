# (tpg) libparted links to libparted-fs-resize and vice-versa
%define _disable_ld_no_undefined 1

%global optflags %{optflags} -Oz

%define major 2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define fsresize_major 0
%define libfsresize %mklibname %{name}-fs-resize %{fsresize_major}

Summary:	Flexible partitioning tool
Name:		parted
Version:	3.5
Release:	3
License:	GPLv3+
Group:		System/Configuration/Hardware
Url:		http://www.gnu.org/software/parted/
Source0:	http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz

# (tpg) patches from SuSE
Patch501:	parted-2.4-ncursesw6.patch
Patch502:	libparted-avoid-libdevice-mapper-warnings.patch
Patch503:	libparted-open-the-device-RO-and-lazily-switch-to-RW.patch
Patch504:	more-reliable-informing-the-kernel.patch
Patch999:	parted-3.5-fix-clang.patch

BuildRequires:	gettext-devel >= 0.18
BuildRequires:	pkgconfig(readline)
BuildRequires:	hostname
BuildRequires:	gperf
BuildRequires:	pkgconfig(devmapper) >= 1.02.153
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(blkid)
Requires:	e2fsprogs

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
%autosetup -p1

%build
autoreconf -fiv
%configure \
	--without-included-regex \
	--enable-device-mapper \
	--enable-static \
	--enable-debug \
	--with-readline \
	--enable-threads=posix \
	--with-packager="%{vendor}" \
	--with-packager-version="%{distro_release}" \
	--with-packager-bug-reports="%{bugurl}" \
	--with-pic

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

%find_lang %{name}

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

%check
# check fails due to /dev not mounted in chroot on bs..
make -C system check || /bin/true

%files -f %{name}.lang
%doc README
%{_sbindir}/parted
%{_sbindir}/partprobe
%doc %{_mandir}/man8/parted.8*
%doc %{_mandir}/man8/partprobe.8*
%doc %{_infodir}/parted.info*

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

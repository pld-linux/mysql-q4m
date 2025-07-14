# TODO
# - port to mysql 5.5 (mysql_priv.h missing)
# - build out of source tree (mysql_priv.h ...)
# - system boost
# - check so linking
# - add -avoid-version to module, install to mysql dir
# - mention support-files/install-exec-hook.txt contents
Summary:	Queue for MySQL is a message queue
Name:		mysql-q4m
Version:	0.9.5
Release:	0.1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://q4m.kazuhooku.com/dist/q4m-%{version}.tar.gz
# Source0-md5:	b7d9f659c0481d808c32f240b7719e1d
Source1:	http://vesta.informatik.rwth-aachen.de/mysql/Downloads/MySQL-5.1/mysql-5.1.55.tar.gz
Patch0:		destdir.patch
URL:		http://q4m.github.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 5.1
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	mysql >= 5.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libqueue_engine.so.0.0.0

%description
Q4M (Queue for MySQL) is a message queue licensed under GPL that works
as a pluggable storage engine of MySQL 5.1, designed to be robust,
fast, flexible.

%prep
%setup -qn q4m-%{version} -a1
%undos Makefile.am
%patch -P0 -p1
ln -s mysql-5.* mysql-src

%build
export CPPFLAGS="%{rpmcppflags} -I/usr/include/mysql"
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-mysql=$(pwd)/mysql-src \
	--disable-static \
	--enable-mmap \
	--prefix=%{_prefix} \
	--with-delete=pwrite \
	--with-sync=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libqueue_engine.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README doc support-files/install.sql
%attr(755,root,root) %{_bindir}/q4m-forward
%attr(755,root,root) %{_libdir}/libqueue_engine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqueue_engine.so.0
%attr(755,root,root) %{_libdir}/libqueue_engine.so

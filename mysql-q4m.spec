# TODO
# - port to mysql 5.5 (mysql_priv.h missing)
# - build out of source tree (mysql_priv.h ...)
Summary:	Queue for MySQL is a message queue
Name:		mysql-q4m
Version:	0.9.5
Release:	0.1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://q4m.kazuhooku.com/dist/q4m-%{version}.tar.gz
# Source0-md5:	b7d9f659c0481d808c32f240b7719e1d
Source1:	http://vesta.informatik.rwth-aachen.de/mysql/Downloads/MySQL-5.1/mysql-5.1.55.tar.gz
# Source1-md5:	e07e79edad557874d0870c914c9c81e1
#Source1:	http://vesta.informatik.rwth-aachen.de/mysql/Downloads/MySQL-5.5/mysql-5.5.11.tar.gz
#Patch0:		build.patch
URL:		http://q4m.github.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mysql-devel >= 5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Q4M (Queue for MySQL) is a message queue licensed under GPL that works
as a pluggable storage engine of MySQL 5.1, designed to be robust,
fast, flexible. It is already in production quality, and is used by
several web services (see Users of Q4M).

%prep
%setup -qn q4m-%{version} -a1
#%patch0 -p1
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
	--enable-mmap \
	--prefix=%{_prefix} \
	--with-delete=pwrite \
	--with-sync=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README doc

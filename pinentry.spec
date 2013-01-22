Summary:	Simple PIN or passphrase entry dialogs
Name:		pinentry
Version:	0.8.2
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2
# Source0-md5:	82e6114e5e27a8ab36f314b332a6e024
Patch0:		0001-Fix-qt4-pinentry-window-created-in-the-background.patch
URL:		http://www.gnupg.org/
BuildRequires:	QtGui-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	libcap-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkg-config
BuildRequires:	qt-build
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details. Base package contains
curses-based dialog.

%package gtk
Summary:	Simple PIN or passphrase entry dialog for GTK+ 1.x
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
Simple PIN or passphrase entry dialog for GTK+ 1.x.

%package qt
Summary:	Simple PIN or passphrase entry dialog for Qt
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description qt
Simple PIN or passphrase entry dialog for Qt.

%prep
%setup -q
%patch0 -p1

cd qt4
%{_bindir}/moc pinentrydialog.h  -o pinentrydialog.moc
%{_bindir}/moc qsecurelineedit.h -o qsecurelineedit.moc
cd ..

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses"
%configure \
	--disable-pinentry-gtk		\
	--disable-pinentry-qt		\
	--enable-fallback-curses	\
	--enable-pinentry-curses	\
	--enable-pinentry-gtk2		\
	--enable-pinentry-qt4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/pinentry

cat >$RPM_BUILD_ROOT%{_bindir}/pinentry <<'EOF'
#!/bin/sh
if [ -n "$PINENTRY_PROGRAM" ]; then
	exec $PINENTRY_PROGRAM "$@"
elif [ -z "$DISPLAY" ]; then
	exec %{_bindir}/pinentry-curses "$@"
elif [ -x %{_bindir}/pinentry-gtk-2 ]; then
	exec %{_bindir}/pinentry-gtk-2 "$@"
elif [ -x %{_bindir}/pinentry-qt4 ]; then
	exec %{_bindir}/pinentry-qt4 "$@"
else
	exec %{_bindir}/pinentry-curses "$@"
fi
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/pinentry
%attr(755,root,root) %{_bindir}/pinentry-curses
%{_infodir}/pinentry.info*

%files gtk
%attr(755,root,root) %{_bindir}/pinentry-gtk-2

%files qt
%attr(755,root,root) %{_bindir}/pinentry-qt4


# NOTE: PLD currently uses netsurf fork (libutf8proc.spec)
# They differ in used buildsystem; netsurf provides .pc file upstream.
Summary:	utf8proc library for NetSurf
Summary(pl.UTF-8):	Biblioteka utf8proc dla projektu NetSurf
Name:		utf8proc
Version:	2.2.0
Release:	0.1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/JuliaStrings/utf8proc/releases
Source0:	https://github.com/JuliaStrings/utf8proc/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4514e50c9973f73375cd059fca22ad8e
Source1:	libutf8proc.pc.in
URL:		https://github.com/JuliaStrings/utf8proc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
utf8proc is a small, clean C library that provides Unicode
normalization, case-folding, and other operations for data in the UTF-8
encoding.

%description -l pl.UTF-8
utf8proc to mała, napisana w czystym C biblioteka zapewniająca
normalizację Unicode, zamianę wielkości liter i inne operacje na
danych w kodowaniu UTF-8.

%package devel
Summary:	Header file for utf8proc library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki utf8proc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for utf8proc library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki utf8proc.

%package static
Summary:	utf8proc static library
Summary(pl.UTF-8):	Statyczna biblioteka utf8proc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
utf8proc static library.

%description static -l pl.UTF-8
Statyczna biblioteka utf8proc.

%prep
%setup -q

%build
%{__make} \
	AR="%{__ar}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	includedir=%{_includedir} \
	libdir=%{_libdir}

# julialang version doesn't provide .pc file
test ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/libutf8proc.pc
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__sed} -e 's,@VERSION@,%{version},' \
	-e 's,@prefix@,%{_prefix},' \
	-e 's,@libdir@,%{_libdir},' %{SOURCE1} >>$RPM_BUILD_ROOT%{_pkgconfigdir}/libutf8proc.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md NEWS.md README.md 
%attr(755,root,root) %{_libdir}/libutf8proc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libutf8proc.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libutf8proc.so
%{_includedir}/utf8proc.h
%{_pkgconfigdir}/libutf8proc.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libutf8proc.a

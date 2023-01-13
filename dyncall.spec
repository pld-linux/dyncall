#
# Conditional build:
%bcond_without	doc	# manual.pdf
#
Summary:	A Generic Dynamic FFI package
Summary(pl.UTF-8):	Ogólny pakiet do dynamicznych wywołań obcych funkcji (FFI)
Name:		dyncall
Version:	1.3
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://dyncall.org/download
Source0:	https://dyncall.org/r%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4f96a2f86aae116f84ee7db01b164d41
Patch0:		%{name}-libdir.patch
# https://dyncall.org/pub/dyncall/dyncall/raw-rev/1e65b8911603
Patch1:		%{name}-cmake.patch
URL:		https://dyncall.org/
BuildRequires:	cmake >= 2.6
%if %{with doc}
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex
# colortbl.sty
BuildRequires:	texlive-latex-extend
BuildRequires:	texlive-latex-moreverb
# for html
#BuildRequires:	texlive-tex4ht
%endif
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 ia64 mips mips64 ppc ppc64 sh sparc sparcv9 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dyncall is a low-level toolkit providing a portable abstraction for
handling native code dynamically at run time.

It comprises three independent components, available as C libraries,
namely:
- 'dyncall' for making function calls,
- 'dyncallback' for writing generic callback handlers, and
- 'dynload' for loading code.

%description -l pl.UTF-8
dyncall to zestaw niskopoziomowych narzędzi z przenośną abstrakcją
dynamicznej obsługi kodu natywnego w czasie uruchomienia.

Obejmuje trzy niezależne komponenty, dostępne jako biblioteki C:
- dyncall do wywołań funkcji
- dyncallback do pisania generycznej obsługi wywołań zwrotnych
- dynload do ładowania kodu

%package doc
Summary:	Documentation for dyncall libraries
Summary(pl.UTF-8):	Dokumentacja bibliotek dyncall
Group:		Documentation
BuildArch:	noarch

%description doc
Documentation for dyncall libraries.

%description doc -l pl.UTF-8
Dokumentacja bibliotek dyncall.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake ..

%{__make}
cd ..

%if %{with doc}
cd doc/manual
%{__make} -f Makefile.generic pdf

# TODO: html (but broken even with SHELL=/bin/bash)
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog LICENSE README ToDo
%{_libdir}/libdyncall_s.a
%{_libdir}/libdyncallback_s.a
%{_libdir}/libdynload_s.a
%{_includedir}/dyncall*.h
%{_includedir}/dynload.h

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/manual/manual.pdf
%endif

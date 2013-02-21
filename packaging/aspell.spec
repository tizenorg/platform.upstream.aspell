#

Name:           aspell
Version:        0.60.6.1
Release:        0
License:        LGPL-2.1+
Summary:        A Free and Open Source Spell Checker
Url:            http://aspell.net/
Group:          Productivity/Text/Spell
Source0:        ftp://ftp.gnu.org/gnu/aspell/%{name}-%{version}.tar.gz
Patch0:         aspell-strict-aliasing.patch
Patch1:         aspell-quotes.patch
Patch2:         aspell-epmty_file.patch
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  gettext-tools
BuildRequires:  libtool
BuildRequires:  ncurses-devel
Recommends:     aspell-en
Suggests:       aspell-ispell
Suggests:       aspell-spell
Provides:       pspell = %{version}
Obsoletes:      pspell < %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(post): info
Requires(preun): info

%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

Its main feature is that it does a much better job of coming up with
possible suggestions than just about any other spell checker available
for the English language, including Ispell and Microsoft Word. It also
has many other technical enhancements over Ispell, such as using shared
memory for dictionaries and intelligently handling personal
dictionaries when more than one Aspell process is open at once.

%package devel
Summary:        Include Files and Libraries Mandatory for Development with aspell
Group:          Development/Libraries/C and C++
Requires:       glibc-devel
Requires:       libaspell = %{version}
Requires:       libpspell15 = %{version}
Provides:       pspell-devel = %{version}
Obsoletes:      pspell-devel < %{version}
Requires(post): info
Requires(preun): info

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require aspell.

%package ispell
Summary:        GNU Aspell - Ispell compatibility
Group:          Productivity/Text/Spell
Requires:       %{name} = %{version}
Conflicts:      ispell

%description ispell
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

This package contains an ispell script for compatibility reasons so that
programs that expect the "ispell" command will work correctly.

%package spell
Summary:        GNU Aspell - Spell compatibility
Group:          Productivity/Text/Spell
Requires:       %{name} = %{version}
Provides:       spell

%description spell
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

This package contains a spell script for compatibility reasons so that programs
that expect the "spell" command will work correctly.

%package -n libaspell
Summary:        GNU Aspell Library
Group:          System/Libraries

%description -n libaspell
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

This package contains the aspell library.

%package -n libpspell15
Summary:        GNU Aspell - Pspell Compatibility Library
Group:          System/Libraries

%description -n libpspell15
GNU Aspell is a spell checker designed to eventually replace Ispell. It
can be used as a library or as an independent spell checker.

This package contains the pspell compatibility library.

%prep
%setup -q
%patch0
%patch1
%patch2

%build
autoreconf -fiv
export CXXFLAGS="%{optflags} `ncursesw6-config --cflags`"
#this is an ugly kludge , don't look :-)
export LDFLAGS="`ncursesw6-config --libs`"
%configure \
    --enable-curses="-lncursesw" \
 --disable-rpath

make %{?_smp_mflags}

%install
%make_install
# Links for compatibility reasons (ispell and spell)
ln -s %{_libdir}/aspell-0.60/ispell %{buildroot}%{_bindir}
ln -s %{_libdir}/aspell-0.60/spell %{buildroot}%{_bindir}
find %{buildroot} -name "*.la" -type f -print -delete
%fdupes -s %{buildroot}

%find_lang %{name}

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info%{ext_info}

%preun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info%{ext_info}

%post devel
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}-dev.info%{ext_info}

%preun devel
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}-dev.info%{ext_info}

%post -n libaspell -p /sbin/ldconfig

%postun -n libaspell -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README TODO
%doc manual/aspell.html/
%{_bindir}/aspell
%{_bindir}/aspell-import
%{_bindir}/pre*
%{_bindir}/run-with-aspell
%{_bindir}/word-list-compress
%doc %{_infodir}/%{name}.info%{ext_info}
%doc %{_mandir}/man1/*.1%{ext_man}
%exclude %{_mandir}/man1/pspell-config.1%{ext_man}

%files devel
%defattr(-,root,root,-)
%doc manual/aspell-dev.html/
%{_bindir}/pspell-config
%{_includedir}/pspell/
%{_includedir}/*.h
%{_libdir}/libaspell.so
%{_libdir}/libpspell.so
%doc %{_infodir}/%{name}-dev.info%{ext_info}
%doc %{_mandir}/man1/pspell-config.1%{ext_man}

%files ispell
%defattr(-,root,root,-)
%{_bindir}/ispell

%files spell
%defattr(-,root,root,-)
%{_bindir}/spell

%files -n libaspell
%defattr(-,root,root,-)
%{_libdir}/aspell-0.60/
%{_libdir}/libaspell.so.15*

%files -n libpspell15
%defattr(-,root,root,-)
%{_libdir}/libpspell.so.15*

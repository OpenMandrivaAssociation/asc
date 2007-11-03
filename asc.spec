%define	name	asc
%define version 2.0.1.0
%define release %mkrel 1
%define	Summary	Advanced Strategic Command

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://heanet.dl.sourceforge.net/sourceforge/asc-hq/%{name}-%{version}.tar.bz2
Source1:	%{name}-16x16.png
Source2:	%{name}-32x32.png
Source3:	%{name}-48x48.png
License:	GPL
Group:		Games/Strategy
URL:		http://www.asc-hq.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL_mixer-devel SDLmm-devel SDL_image-devel
BuildRequires:	bzip2-devel jpeg-devel
BuildRequires:  libsigc++1.2-devel
BuildRequires:  libgii-devel

%description
ASC is a free, turn based strategy game. It is designed in the tradition
of the Battle Isle series from Bluebyte.

%prep
%setup -q
# there seems to be a conflict with libintl defines
# find . -type f -exec perl -pi -e 's/gettext/gettex_/g' {} \;

%build
%configure2_5x	--enable-genparse \
		--disable-paragui \
		--bindir=%{_gamesbindir} 
%{__perl} -pi -e 's|^SUBDIRS = (.*)music(.*)|SUBDIRS = $1 $2|' data/Makefile
%make

%install
%{__rm} -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir}

%{__install} -d $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{Summary}
Comment=%{Summary}
Exec=%_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Games-Strategy;Game;StrategyGame;
EOF

%{__install} %{SOURCE1} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
%{__install} %{SOURCE2} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
%{__install} %{SOURCE3} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%update_menus

%postun
%clean_menus

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}*
%defattr(644,root,root,755)
%doc README COPYING AUTHORS doc/
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man6/*

%define	name	asc
%define version 2.4.0.0
%define release %mkrel 5
%define	Summary	Advanced Strategic Command

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://heanet.dl.sourceforge.net/sourceforge/asc-hq/%{name}-%{version}.tar.bz2
Source1:	%{name}-16x16.png
Source2:	%{name}-32x32.png
Source3:	%{name}-48x48.png
#Patch0:		fix_sg_cpp.patch
Patch1:		fix_textfile_evaluation_cpp.patch
#Patch2:		fix_edmain_cpp.patch
Patch3:		fix_mount_cpp.patch
Patch4:		asc-2.4.0.0-fix-str-fmt.patch
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.asc-hq.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL_mixer-devel
#BuildRequires:	SDLmm-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_sound-devel
BuildRequires:	bzip2-devel jpeg-devel
BuildRequires:  libsigc++1.2-devel
BuildRequires:  libgii-devel
BuildRequires:  boost-devel
BuildRequires:  freetype2-devel
BuildRequires:  expat-devel
BuildRequires:  libphysfs-devel
BuildRequires:  png-devel
BuildRequires:  lua-devel
BuildRequires:	libwxgtk2.8-devel
BuildRequires:  zip

%description
ASC is a free, turn based strategy game. It is designed in the tradition
of the Battle Isle series from Bluebyte.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p0
# there seems to be a conflict with libintl defines
# find . -type f -exec perl -pi -e 's/gettext/gettex_/g' {} \;

%build
%configure2_5x	--enable-genparse \
		--disable-paragui \
		--bindir=%{_gamesbindir} 
%{__perl} -pi -e 's|^SUBDIRS = (.*)music(.*)|SUBDIRS = $1 $2|' data/Makefile
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall bindir=%{buildroot}%{_gamesbindir}

%{__install} -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{Summary}
Comment=%{Summary}
Exec=%_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;StrategyGame;
EOF

%{__install} %{SOURCE1} -D %{buildroot}%{_miconsdir}/%{name}.png
%{__install} %{SOURCE2} -D %{buildroot}%{_iconsdir}/%{name}.png
%{__install} %{SOURCE3} -D %{buildroot}%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
%{__rm} -rf %{buildroot}

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

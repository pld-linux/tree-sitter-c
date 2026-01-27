#
# Conditional build:
%bcond_without	python3	# Python 3.x binding
%bcond_without	tests	# Python binding load test

Summary:	C grammar for tree-sitter
Summary(pl.UTF-8):	Gramatyka języka C dla tree-sittera
Name:		tree-sitter-c
Version:	0.24.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/tree-sitter/tree-sitter-c/releases
Source0:	https://github.com/tree-sitter/tree-sitter-c/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e399309a829fa3bcb09609c9de2472f2
URL:		https://github.com/tree-sitter/tree-sitter-c
# c11
BuildRequires:	gcc >= 6:4.7
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-tree-sitter >= 0.24
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		soname_ver	15.0

%description
C grammar for tree-sitter.

%description -l pl.UTF-8
Gramatyka języka C dla tree-sittera.

%package devel
Summary:	Header files for tree-sitter-c
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tree-sitter-c
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-c.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tree-sitter-c.

%package static
Summary:	Static tree-sitter-c library
Summary(pl.UTF-8):	Statyczna biblioteka tree-sitter-c
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-c library.

%description static -l pl.UTF-8
Statyczna biblioteka tree-sitter-c.

%package -n neovim-parser-c
Summary:	C parser for Neovim
Summary(pl.UTF-8):	Analizator składni języka C dla Neovima
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-c
C parser for Neovim.

%description -n neovim-parser-c -l pl.UTF-8
Analizator składni języka C dla Neovima.

%package -n python3-tree-sitter-c
Summary:	C parser for Python
Summary(pl.UTF-8):	Analizator składni języka C dla Pythona
Group:		Libraries/Python
Requires:	python3-tree-sitter >= 0.24

%description -n python3-tree-sitter-c
C parser for Python.

%description -n python3-tree-sitter-c -l pl.UTF-8
Analizator składni języka C dla Pythona.

%prep
%setup -q

%build
%{__make} \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__python3} -m unittest discover -s bindings/python/tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_libdir}/nvim/parser}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} ../../libtree-sitter-c.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/c.so

# redundant symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-c.so.15

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/tree_sitter_c/*.c
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{_libdir}/libtree-sitter-c.so.%{soname_ver}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-c.so
%{_includedir}/tree_sitter/tree-sitter-c.h
%{_pkgconfigdir}/tree-sitter-c.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-c.a

%files -n neovim-parser-c
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/c.so

%if %{with python3}
%files -n python3-tree-sitter-c
%defattr(644,root,root,755)
%dir %{py3_sitedir}/tree_sitter_c
%{py3_sitedir}/tree_sitter_c/_binding.abi3.so
%{py3_sitedir}/tree_sitter_c/__init__.py
%{py3_sitedir}/tree_sitter_c/__init__.pyi
%{py3_sitedir}/tree_sitter_c/py.typed
%{py3_sitedir}/tree_sitter_c/__pycache__
%{py3_sitedir}/tree_sitter_c/queries
%{py3_sitedir}/tree_sitter_c-%{version}-py*.egg-info
%endif

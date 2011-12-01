%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define srcname FormEncode

Name:           python-formencode
Version:        1.2.2
Release:        2.1%{?dist}
Summary:        HTML form validation, generation, and convertion package  

Group:          Development/Libraries
License:        Python
URL:            http://formencode.org/
Source0:        http://cheeseshop.python.org/packages/source/F/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

Requires: python-setuptools
BuildRequires: python-devel
BuildRequires: python-setuptools-devel
BuildRequires: python-docutils
BuildRequires: python-nose

# ElementTree is part of python2.5 on FC7+
# This is also needed for EL-5
%if 0%{?fedora} <= 6 && 0%{?rhel} < 6
BuildRequires:   python-elementtree
Requires:   python-elementtree
%endif

%description
FormEncode validates and converts nested structures. It allows for a 
declarative form of defining the validation, and decoupled processes 
for filling and generating forms.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

# Build the docs then throw out the script
pushd docs
sed -i 's/rst2html.py/rst2html/' build
./build
rm -rf build
popd

# bah.  setuptools resource badness
# Luckily ian bicking wrote the lookup for this to correctly fallback on the
# system catalog
for file in $RPM_BUILD_ROOT%{python_sitelib}/formencode/i18n/* ; do
    if [ -d $file ] ; then
        if [ -e $file/LC_MESSAGES/%{srcname}.mo ] ; then
            mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/`basename $file`/LC_MESSAGES/
            mv $file/LC_MESSAGES/%{srcname}.mo $RPM_BUILD_ROOT%{_datadir}/locale/`basename $file`/LC_MESSAGES/
        fi
    fi
done
rm -rf $RPM_BUILD_ROOT%{python_sitelib}/formencode/i18n

%find_lang %{srcname}

%clean
rm -rf $RPM_BUILD_ROOT

%check
PYTHONPATH=$(pwd) nosetests

%files -f %{srcname}.lang
%defattr(-,root,root,-)
%doc PKG-INFO docs
%{python_sitelib}/formencode
%{python_sitelib}/%{srcname}-%{version}-py%{pyver}.egg-info

%changelog
* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2.2-2.1
- Fix conditional for RHEL

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Luke Macken <lmacken@redhat.com> -1.2.2-1
- Update to 1.2.2
- Conditionalize python-elementtree requirement

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> - 1.2-1
- Update to 1.2
- Run the test suite
- Remove formencode-translations-system.patch

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.1-3
- Rebuild for Python 2.6

* Thu Aug 28 2008 Toshio Kuratomi <toshio@fedoraproject.org> 1.0.1-2
- Clean up license tag
- Fix executable in %%doc
- Move translations to the proper directory

* Fri Jul 11 2008 Toshio Kuratomi <toshio@fedoraproject.org> 1.0.1-1
- Update to 1.0.1
- Fixes issue where chained_validators were silently ignored.  (bz#454988)
  Both of our patches are fixed upstream now.

* Tue Mar 18 2008 Luke Macken <lmacken@redhat.com> 1.0-1
- Update to 1.0

* Fri Feb 29 2008 Luke Macken <lmacken@redhat.com> 0.9-2
- Add a patch to not explicitly use python2.4

* Thu Feb 28 2008 Luke Macken <lmacken@redhat.com> 0.9-1
- Update to 0.9

* Sun Sep  2 2007 Luke Macken <lmacken@redhat.com> 0.7.1-2
- Update for python-setuptools changes in rawhide

* Mon Apr  9 2007 Toshio Kuratomi <toshio@tiki-lounge.com> 0.7.1-1
- Upgrade to bugfix 0.7.1 release.

* Fri Apr  6 2007 Toshio Kuratomi <toshio@tiki-lounge.com> 0.7-3
- Require python-setuptools

* Sat Mar  3 2007 Luke Macken <lmacken@redhat.com> 0.7-2
- Rebuild with newer badurl patch

* Sat Mar  3 2007 Luke Macken <lmacken@redhat.com> 0.7-1
- 0.7

* Sat Dec  9 2006 Luke Macken <lmacken@redhat.com> 0.6-3
- Rebuild for python 2.5

* Fri Nov  3 2006 Luke Macken <lmacken@redhat.com> 0.6-2
- Rebuild

* Fri Nov  3 2006 Luke Macken <lmacken@redhat.com> 0.6-1
- 0.6

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> 0.5.1-3
- Rebuild for FC6

* Sat Jul 29 2006 Luke Macken <lmacken@redhat.com> 0.5.1-2
- Rebuild

* Sat Jul 29 2006 Luke Macken <lmacken@redhat.com> 0.5.1-1
- 0.5.1

* Sat Feb  4 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.4-2
- Fix build on devel
- Switch to unmanaged egg

* Thu Dec 29 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.4-1
- Upstream update

* Sun Oct 23 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.2.2-3
- fixed some minor packaging issues

* Tue Oct 13 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.2.2-2
- fixed the too long description line
- add -O1 to the installation process
- %%ghost'ed the *.pyo files

* Tue Oct 06 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.2.2-1
- update to upstream version 0.2.2

* Tue Sep 20 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.2.1-2
- fixed some minor packaging issues for review.

* Tue Sep 20 2005 Oliver Andrich <oliver.andrich@gmail.com> 0.2.1-1
- initial creation
- Version 0.2.1

# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.15.2)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x01\x3e\
\x3c\
\x3f\x78\x6d\x6c\x20\x76\x65\x72\x73\x69\x6f\x6e\x3d\x22\x31\x2e\
\x30\x22\x20\x3f\x3e\x3c\x73\x76\x67\x20\x68\x65\x69\x67\x68\x74\
\x3d\x22\x34\x38\x22\x20\x76\x69\x65\x77\x42\x6f\x78\x3d\x22\x30\
\x20\x30\x20\x34\x38\x20\x34\x38\x22\x20\x77\x69\x64\x74\x68\x3d\
\x22\x34\x38\x22\x20\x78\x6d\x6c\x6e\x73\x3d\x22\x68\x74\x74\x70\
\x3a\x2f\x2f\x77\x77\x77\x2e\x77\x33\x2e\x6f\x72\x67\x2f\x32\x30\
\x30\x30\x2f\x73\x76\x67\x22\x3e\x3c\x70\x61\x74\x68\x20\x64\x3d\
\x22\x4d\x30\x20\x30\x68\x34\x38\x76\x34\x38\x68\x2d\x34\x38\x7a\
\x22\x20\x66\x69\x6c\x6c\x3d\x22\x6e\x6f\x6e\x65\x22\x2f\x3e\x3c\
\x70\x61\x74\x68\x20\x64\x3d\x22\x4d\x33\x32\x20\x32\x68\x2d\x32\
\x34\x63\x2d\x32\x2e\x32\x31\x20\x30\x2d\x34\x20\x31\x2e\x37\x39\
\x2d\x34\x20\x34\x76\x32\x38\x68\x34\x76\x2d\x32\x38\x68\x32\x34\
\x76\x2d\x34\x7a\x6d\x36\x20\x38\x68\x2d\x32\x32\x63\x2d\x32\x2e\
\x32\x31\x20\x30\x2d\x34\x20\x31\x2e\x37\x39\x2d\x34\x20\x34\x76\
\x32\x38\x63\x30\x20\x32\x2e\x32\x31\x20\x31\x2e\x37\x39\x20\x34\
\x20\x34\x20\x34\x68\x32\x32\x63\x32\x2e\x32\x31\x20\x30\x20\x34\
\x2d\x31\x2e\x37\x39\x20\x34\x2d\x34\x76\x2d\x32\x38\x63\x30\x2d\
\x32\x2e\x32\x31\x2d\x31\x2e\x37\x39\x2d\x34\x2d\x34\x2d\x34\x7a\
\x6d\x30\x20\x33\x32\x68\x2d\x32\x32\x76\x2d\x32\x38\x68\x32\x32\
\x76\x32\x38\x7a\x22\x2f\x3e\x3c\x2f\x73\x76\x67\x3e\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00\x70\x37\
\x00\x69\
\x00\x6d\x00\x67\
\x00\x06\
\x07\x03\x7d\xc3\
\x00\x69\
\x00\x6d\x00\x61\x00\x67\x00\x65\x00\x73\
\x00\x0d\
\x0e\xae\xb0\x87\
\x00\x63\
\x00\x6f\x00\x70\x00\x79\x00\x5f\x00\x69\x00\x63\x00\x6f\x00\x6e\x00\x2e\x00\x73\x00\x76\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x8b\xe0\x31\xc5\x95\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
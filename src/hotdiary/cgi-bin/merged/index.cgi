#!/bin/ksh


#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  


#
# FileName: mergedindex.cgi
# Purpose: it invokes webpage.cgi
# Creation Date: 05-30-99 
# Created by: Smitha Gudur
# 


. /usr/local/hotdiary/config/hd.env
#export PATH=$PATH:/usr/local/bin:/usr/gnu/bin
export PERL5LIB=$HDHOME/perllibs
./mergedwebpage.cgi

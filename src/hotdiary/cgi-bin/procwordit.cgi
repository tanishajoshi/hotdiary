#!/usr/bin/perl

# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.

## processwordit.cgi

use ParseTem::ParseTem;
require "cgi-lib.pl";
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;
use utils::utils;


&ReadParse(*input);

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

# bind invoicetab table vars
   tie %invoicetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/aux/invoicetab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['counter', 'index' ] };

$prml = "";
#$firstname = $logtab{$login}{fname};
#$lastname = $logtab{$login}{lname};
#$street = $logtab{$login}{street};
#$city = $logtab{$login}{city};
#$state = $logtab{$login}{state};
#$zipcode = $logtab{$login}{zipcode};
#$country = $logtab{$login}{country};
#$email = $logtab{$login}{email};

$invoice = $invoicetab{counter}{index};
$invoice = $invoice + 1;
$invoicetab{counter}{index} = $invoice;
tied(%invoicetab)->sync();
$prml = strapp $prml, "firstname=$firstname";
$prml = strapp $prml, "login=$login";
$prml = strapp $prml, "lastname=$lastname";
$prml = strapp $prml, "street=$street";
$prml = strapp $prml, "city=$city";
$prml = strapp $prml, "state=$state";
$prml = strapp $prml, "zipcode=$zipcode";
$prml = strapp $prml, "country=$country";
$prml = strapp $prml, "invoicenum=$invoice";
$prml = strapp $prml, "email=$email";
$amount = "5.99";

$prml = strapp $prml, "amount=$amount";
$prml = strapp $prml, "product=WordIt!";
$prml = strapp $prml, "x_description=WordIt";

$custid = "$invoice-$$";
$prml = strapp $prml, "x_Cust_ID=$custid";

$prml = strapp $prml, "template=$ENV{HDTMPL}/cardprocess.html";
$prml = strapp $prml, "templateout=$ENV{HDHOME}/tmp/cardprocess-$$.html";

parseIt $prml;

hdsystemcat "$ENV{HDHOME}/tmp/cardprocess-$$.html";

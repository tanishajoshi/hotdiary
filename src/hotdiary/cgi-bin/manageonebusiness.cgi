#!/usr/bin/perl

#
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
#

#
# FileName: manageonebusiness.cgi
# Purpose: Top screen for virtual business 
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
#use UNIVERSAL qw(isa);
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = $ENV{HDCOOKIE_TIMEOUT};

   hddebug("manageonebusiness.cgi");

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp}; 
   if ($vdomain eq "") {
      $vdomain = "www.hotdiary.com";
   } 
   $os = $input{os}; 
   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);


   tie %jivetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/jivetab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['url', 'logo', 'title', 'banner', 'regusers', 
	'account', 'topleft', 'topright', 'middleright', 
	'bottomleft', 'bottomright', 'meta'] };
                                                                              
   $hs = $input{'hs'};
   $biscuit = $input{'biscuit'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }         

   if ($biscuit eq "") {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
              status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	      exit;
	    } 
	 }
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Your login session information is missing. Perhaps you are simply viewing a published calendar website. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   }

   # bind session table vars
   tie %sesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/sesstab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['biscuit', 'login', 'time'] };

# bind logsess table vars
   tie %logsess, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logsess",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['login', 'biscuit'] };                                       

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 
	'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      if ($hs eq "") {
	 if ($jp ne "") {
            if ($jp ne "buddie") {
               status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
               exit;
	    } 
         }
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      } else {
         status("Invalid session or session does not exist. Please relogin.  Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
      }
      exit;
   } else {
      if ($login eq "") {
         $login = $sesstab{$biscuit}{'login'};
         if ($login eq "") {
            error("Login is an empty string. Possibly invalid session.\n");
            exit;
	 }
      }
   }

   if ((time() - $sesstab{$biscuit}{'time'}) > $SESSION_TIMEOUT) {
      delete $sesstab{$biscuit};
      delete $logsess{$login};
      if ($hs eq "") {
         if ($jp ne "") {
	    if ($jp ne "buddie") {
               status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already expired. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }
   $HDLIC = $input{'HDLIC'};
   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

   $sesstab{$biscuit}{'time'} = time();

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
   
      if (!(exists $lictab{$HDLIC})) {
         status("You do not have a valid license to use the application.");
         exit;
      } else {
         if ($lictab{$HDLIC}{'vdomain'} eq "") {
            $lictab{$HDLIC}{'vdomain'} = "\L$vdomain";
            $ip = $input{'ip'};
            $lictab{$HDLIC}{'ip'} = "\L$ip";
         } else {
              if ("\L$lictab{$HDLIC}{'vdomain'}" ne "\L$vdomain") {
                 status("You have a valid license, however this product was installed on a domain that is different from $vdomain. Please contact HotDiary.com, and they will be happy to help you with the license.");
                 exit;
              }
         }
      }
   }
 
   tie %parttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/partners/parttab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['logo', 'title', 'banner'] };

   if (exists $jivetab{$jp}) {
      $logo = $jivetab{$jp}{logo};
      $label = $jivetab{$jp}{title};
   } else {
      if (exists $lictab{$HDLIC}) {
         $partner = $lictab{$HDLIC}{partner};
         if (exists $parttab{$partner}) {
            $logo = $parttab{$partner}{logo};
            $label = $parttab{$partner}{title};
         }
      }
   }

   $business = trim $input{'business'};
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $business = trim $input{'business'};
   if ($os ne "nt") {
      $execbusiness = encurl "execbusiness.cgi";
      $execcreatebusiness = encurl "execcreatebusiness.cgi";
      $execmanagebusiness = encurl "execmanagebusiness.cgi";
   } else {
      $execbusiness = "execbusiness.cgi";
      $execcreatebusiness = "execcreatebusiness.cgi";
      $execmanagebusiness = "execmanagebusiness.cgi";
   }

   if ($business eq "") {
      status("$login: Please select a business to manage. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?p0=$execbusiness&p1=biscuit&p2=f&pnum=4&p3=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&f=mc&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to Manage business."); 
      exit;
   }

   if (!exists ($businesstab{$business})) {
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execcreatebusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
     exit;
   }
   if ($login ne $businesstab{$business}{businessmaster}) {
      if (-d "$ENV{HDDATA}/business/business/$business/managertab") {
         tie %managertab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
           SUFIX => '.rec',
           SCHEMA => {
           ORDER => ['login']};
         if (!exists($managertab{$login})) {   
            status("$login: You do not have permission to manage ($business) business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
           exit;
         }
      } else {
         status("$login: You do not have permission to manage ($business) business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execmanagebusiness&p1=biscuit&p2=business&p3=jp&business=$business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage Business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execbusiness&p1=biscuit&p2=jp&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
         exit;
      }
   }

   #$password = $input{password};
   #$password_required = 0;
   #$pwd_file = 0;

   #if (-d "$ENV{HDDATA}/business/business/$business/mgraccesstab") {
   #      tie %mgraccesstab, 'AsciiDB::TagFile',
   #   DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
   #   SUFIX => '.rec',
   #   SCHEMA => {
   #   ORDER => ['pbusinessmaster', 'pbusinessmanager', 'pother', 'invite',
   #             'approve', 'delete', 'edit', 'manage', 'contact',
   #		 'teams'] };
   #   $pwd_file = 1;
   #}

   #if ($pwd_file == 1) {
   #   if ($login eq $businesstab{$business}{businessmaster}) {
   #      if ($mgraccesstab{access}{pbusinessmaster} eq "CHECKED") {
   #         $password_required = 1;
   #      }
   #   }
#
#      if ($password_required == 0 ) {
#         if (-d "$ENV{HDDATA}/business/business/$business/managertab") {
#            tie %managertab, 'AsciiDB::TagFile',
#            DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
#            SUFIX => '.rec',
#            SCHEMA => {
#            ORDER => ['login']};
#
#           if (exists($managertab{$login})) {
#              if ($mgraccesstab{access}{pbusinessmanager} eq "CHECKED") {
#                 $password_required = 1;
#              }
#           } else {
#              if ($mgraccesstab{access}{pother} eq "CHECKED") {
#                 $password_required = 1;
#              }
#           }
#         }
#      }
#   }
#
#   if ($password_required == 1) {
#      if ($password ne $businesstab{$business}{password}) {
#         status("$login: Please enter the correct password. Your password ($password) is not correct. <BR>If you have lost password or forgotten your password for ($business), contact hotdiary.com specifying your (login) and ($business). <BR>Password will be sent to your email address of your member account. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=4&p0=$execmanagebusiness&p1=biscuit&p2=business&p3=jp&business=$business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=0s&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage Business."); 
#         exit;
#      } 
#   }
  
   $prml = "";
   if ($logo ne "") {
         $logo = adjusturl $logo;
   }
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "logo=$logo";
   $prml = strapp $prml, "label=$label";
   $sc = $input{sc};
   if ($os ne "nt") {
      $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
      $prml = strapp $prml, "formenc=$formenc";
      $execproxylogout = encurl "/proxy/execproxylogout.cgi";
      $execdeploypage =  encurl "execdeploypage.cgi";
      $execshowtopcal =  encurl "execshowtopcal.cgi";
      $execshowpendingreq =  encurl "execshowpendingreq.cgi";
      $execmanageresourcesbusiness =  encurl "execmanageresourcesbusiness.cgi";
      $execeditbusiness = encurl "execeditbusiness.cgi";
      $execaccesscontrolbusiness = encurl "execaccesscontrolbusiness.cgi";
      $execmanagepeopleinbusiness =  encurl "execmanagepeopleinbusiness.cgi";
   } else {
      $prml = strapp $prml, "formenc=";
      $execproxylogout =  "/proxy/execproxylogout.cgi";
      $execdeploypage =  "execdeploypage.cgi";
      $execshowtopcal =  "execshowtopcal.cgi";
      $execshowpendingreq =  "execshowpendingreq.cgi";
      $execmanageresourcesbusiness =  "execmanageresourcesbusiness.cgi";
      $execeditbusiness =  "execeditbusiness.cgi";
      $execaccesscontrolbusiness = "execaccesscontrolbusiness.cgi";
      $execmanagepeopleinbusiness =  "execmanagepeopleinbusiness.cgi";
   }
   $alphaindex = substr $login, 0, 1;
   $alphaindex = $alphaindex . '-index';

   $prml = strapp $prml, "template=$ENV{HDTMPL}/manageonebusiness.html";
   $prml = strapp $prml, "templateout=$ENV{HDHREP}/$alphaindex/$login/manageonebusiness-$$.html";
   $prml = strapp $prml, "biscuit=$biscuit";
   if ($sc eq "p") {
      $welcome = "Calendar Of";
   } else {
      $welcome = "Welcome";
   }
   $prml = strapp $prml, "welcome=$welcome";
   $prml = strapp $prml, "login=$login";
   $prml = strapp $prml, "HDLIC=$HDLIC";
   $prml = strapp $prml, "ip=$ip";
   $prml = strapp $prml, "rh=$rh";
   $prml = strapp $prml, "hs=$hs";
   $prml = strapp $prml, "vdomain=$vdomain";
   $prml = strapp $prml, "business=$business";
   $prml = strapp $prml, "jp=$jp";
   $prml = strapp $prml, "execaccesscontrolbusiness=$execaccesscontrolbusiness";
   $prml = strapp $prml, "execshowpendingreq=$execshowpendingreq";
   $prml = strapp $prml, "execmanageresourcesbusiness=$execmanageresourcesbusiness";
   $prml = strapp $prml, "execeditbusiness=$execeditbusiness";
   $prml = strapp $prml, "execmanagepeopleinbusiness=$execmanagepeopleinbusiness";
   $prml = strapp $prml, "execproxylogout=$execproxylogout";
   $prml = strapp $prml, "execdeploypage=$execdeploypage";
   $prml = strapp $prml, "execshowtopcal=$execshowtopcal";

   parseIt $prml;

   #system "cat $ENV{HDTMPL}/content.html";
   #system "cat $ENV{HDHREP}/$alphaindex/$login/manageonebusiness.html";
   hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/manageonebusiness-$$.html";


   tied(%sesstab)->sync();
   tied(%logsess)->sync();

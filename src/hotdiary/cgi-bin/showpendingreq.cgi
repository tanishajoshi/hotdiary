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
# FileName: showpendingreq.cgi 
# Purpose: Create A Virtual Intranet
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

   #print &PrintHeader;
   #print &HtmlTop ("showpendingreq.cgi ");
   hddebug ("showpendingreq.cgi ");

   $vdomain = trim $input{'vdomain'};
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
               status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login again.");
	       exit;
            }
         } 
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      } else {
         status("$login: Your session has already timed out. However, all your personal information is completely intact. Click <a href=\"http://$vdomain/$hs/$icgi\" target=\"_parent\"> here</a> to login again.");
      }
      exit;
   }

   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $HDLIC = $input{'HDLIC'};
      # bind login table vars
      tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };
   
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
  
   tie %businesstab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/business/businesstab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
        'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
        'fax', 'url', 'email', 'other', 'list'] };


   $business = trim $input{business};
   $rh = $input{rh};
   if ($os ne "nt") {
         $execbusiness = encurl "execbusiness.cgi";
         $execmanageonebusiness = encurl "execmanageonebusiness.cgi";
   } else {
         $execbusiness = "execbusiness.cgi";
         $execmanageonebusiness = "execmanageonebusiness.cgi";
   }

   if ((!exists $businesstab{$business}) || ($business eq "")) {   
      if ($os ne "nt") {
         $execcreatebusiness = encurl "execcreatebusiness.cgi";
      } else {
         $execcreatebusiness = "execcreatebusiness.cgi";
      }
      status("$login: Business ($business) does not exist. Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execcreatebusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to create business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to business home.");
      exit;        
   }

   if ($login ne $businesstab{$business}{businessmaster}) {
      tie %mgraccesstab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/business/business/$business/mgraccesstab",
        SUFIX => '.rec',
        SCHEMA => {
        ORDER => ['access', 'pbusinessmaster', 'pbusinessmanager', 'pother',
		 'invite', 'approve', 'delete', 'edit', 'manage', 
		'contact', 'teams']};

      tie %managertab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$business/managertab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['login']};

     if (!exists($managertab{$login})) {
         status("$login: You do not have the permission to approve pending requests.  <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execmanageonebusiness&p1=biscuit&p2=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business.");
         exit;
     };

     if ($mgraccesstab{access}{approve} ne "CHECKED") {
        status("$login: You do not have the permission to approve pending requests. Manager role settings donot allow to approve pending requests to join business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execmanageonebusiness&p1=biscuit&p2=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business.");
        exit;
     }
  }


  if ($logo ne "") {
     $logo = adjusturl $logo;
  }
  $sc = $input{sc};


   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=dddddd>";
   $msg .= "<TD></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">First Name</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">Last Name</FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;
   $cntr = 0;

   if (!(-d "$ENV{HDDATA}/business/business/$business/pendingtab")) {
      status("$login: ($business) currently does not have any pending requests to join. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execmanageonebusiness&p1=biscuit&p2=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business."); 
      exit; 
   }

   tie %pendingtab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/business/business/$business/pendingtab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER => ['business']};

   foreach $mem (sort keys %pendingtab) {
      $cntr = $cntr +1;
      $msg = "<TR>";
      $msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=CHECKBOX NAME=$mem></FONT></TD>";
      $pending .= $mem;
      $pending .= " ";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$logtab{$mem}{'fname'} &nbsp;</FONT></TD>";
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$logtab{$mem}{'lname'} &nbsp;</FONT></TD>";
      $msg .= "</TR>";

      if (exists $logtab{$mem}) {
         $smsg .= $msg;
      } else {
          $umsg .= $msg;
      }
   }


   if ($cntr == 0) {
      status("$login: ($business) currently does not have any pending requests to join. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=3&p0=$execmanageonebusiness&p1=biscuit&p2=business&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&business=$business&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to manage business. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.cgi?pnum=2&p0=$execbusiness&p1=biscuit&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to return to Business home.");
      exit;
   }

   (@hshpending) = split " ", $pending; 
   foreach $cn (@hshpending) {
       $cn = trim $cn;
   }
 
      $smsg .= "</TABLE>";
      $umsg .= "</TABLE>";
      $smsg = adjusturl $smsg;

      $prb = "";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "logo=$logo";
      $prb = strapp $prb, "label=$label";
      if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"application/x-www-form-urlencoded\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execapprovepending = encurl "execapprovepending.cgi";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";
      } else {
         $prb = strapp $prb, "formenc=";
         $execapprovepending = "execapprovepending.cgi";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
      }

      $alphaindex = substr $login, 0, 1;
      $alphaindex = $alphaindex . '-index';

      $prb = strapp $prb, "template=$ENV{HDTMPL}/showpendingreq.html";
      $prb = strapp $prb, "templateout=$ENV{HDHREP}/$alphaindex/$login/showpendingreq-$$.html";
      $prb = strapp $prb, "biscuit=$biscuit";
      $welcome = "Welcome";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "vdomain=$vdomain";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execapprovepending\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=business>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=approve>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=numbegin>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=numend>";

      #values of checkboxes as each parameter
      $k = 0;
      $mcntr = 6;
      $numend = $mcntr;
      $numbegin = $mcntr;
      # this tells from where the parameter for selection starts
      foreach $cn (@hshpending) {
         $cn = trim $cn;
	 $numend = $numend + 1;
	 $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=box$k>";
	 $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=box$k VALUE=$cn>";
         $mcntr = $mcntr + 1;
         $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=$cn>";
         hddebug ("pmcntr = p$mcntr");
         $mcntr = $mcntr + 1;
         $k = $k + 1;
      }
      $numend = $numend - 1;

      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=$mcntr>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=business VALUE=$business>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numend VALUE=$numend>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=numbegin VALUE=$numbegin>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=enum VALUE=6>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re0 VALUE=CGISUBDIR>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le0 VALUE=rh>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re1 VALUE=HTTPSUBDIR>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le1 VALUE=hs>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re2 VALUE=SERVER_NAME>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le2 VALUE=vdomain>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re3 VALUE=HDLIC>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le3 VALUE=HDLIC>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le4 VALUE=os>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re4 VALUE=os>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=le5 VALUE=HTTP_COOKIE>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=re5 VALUE=HTTP_COOKIE>";

      $hiddenvars = adjusturl $hiddenvars;
      $prb = strapp $prb, "hiddenvars=$hiddenvars";
      $prb = strapp $prb, "business=$business";
      $prb = strapp $prb, "members=$smsg";
      $prb = strapp $prb, "execproxylogout=$execproxylogout";
      $prb = strapp $prb, "execdeploypage=$execdeploypage";
      $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
      parseIt $prb;
      #system "cat $ENV{HDTMPL}/content.html";
      #system "cat $ENV{HDHREP}/$alphaindex/$login/showpendingreq.html";
      hdsystemcat "$ENV{HDHREP}/$alphaindex/$login/showpendingreq-$$.html";

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();

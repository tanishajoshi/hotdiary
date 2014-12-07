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
# FileName: groupcontact.cgi 
# Purpose: Create a group contact
# Creation Date: 09-11-99
# Created by: Smitha Gudur
#

require "cgi-lib.pl";
use ParseTem::ParseTem;
use tparser::tparser;
use AsciiDB::TagFile;            
use utils::utils;
use calutil::calutil;
use calfuncs::calfuncs;   
use scheduleresolve::scheduleresolve;   

# Read in all the variables set by the form
   &ReadParse(*input);

#session timeout in secs
   $SESSION_TIMEOUT = 3600;

   #print &PrintHeader;
   #print &HtmlTop ("groupcontact.cgi ");
   hddebug ("groupcontact.cgi ");

   $vdomain = trim $input{'vdomain'};
   $rh = $input{rh};
   $jp = $input{jp}; 
   hddebug "jp = $jp";
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

   $g = $input{g};
   $g = "\L$g";
   # bind leditgrouptab table vars
   tie %leditgrouptab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/leditgrouptab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'jiveit', 'publicedit' ] };

   $publicedit = 0;
   if (exists($leditgrouptab{$g}) ) {
      if ($jp eq "") {
         $jp = $leditgrouptab{$g}{jiveit};
      }
   }

   $sc = $input{sc}; 
   if ($biscuit eq "") {
      if ( ($g ne "") && (exists $leditgrouptab{$g}) && 
           ($leditgrouptab{$g}{publicedit} eq "CHECKED") ) {
         $publicedit = 1;
      } else {
         hddebug "Came here unfortunately";
         $sc = "p";
      }
   }
   hddebug "g = $g, publicedit = $publicedit";
  
  # check if session record exists.
   if ($publicedit == 0) {
      if ($sc ne "p") {
         if ($biscuit eq "") {
            if ($hs eq "") {
	       if ($jp ne "") {
                  if ($jp ne "buddie") {
                 status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\"> here</a> to login.\n");
	         exit;
	          }    
	       }
               status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
            } else {
               status("Your login session information is missing. Click <a href=\"http://$vdomain/$hs/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
            }
            exit;
         }
      }
   }

 
   if ($publicedit == 0 ) {
      if (($biscuit ne "") && ($sc ne "p") ) { 
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
         # reset the timer.
         $sesstab{$biscuit}{'time'} = time();
      }
   }

   $alpha = substr $jp, 0, 1;
   $alpha = $alpha . '-index';


   if ($publicedit == 1) {
      system "mkdir -p $ENV{HTTPHOME}/html/hd/contacts/$g";
      system "chmod 755 $ENV{HTTPHOME}/html/hd/contacts/$g";

      if (!-f ( "$ENV{HTTPHOME}/html/hd/contacts/$g/index.cgi") ){
          system "ln -s $ENV{HDCGI}/contacts/index.cgi $ENV{HTTPHOME}/html/hd/contacts/$g";
      }
      if (!-f ( "$ENV{HTTPHOME}/html/hd/contacts/$g/webpage.cgi") ){
          system "ln -s $ENV{HDCGI}/contacts/webpage.cgi $ENV{HTTPHOME}/html/hd/contacts/$g";
      }

      if (!-d ( "$ENV{HTTPHOME}/html/hd/addressbook/$g") ) {
         system "ln -s $ENV{HTTPHOME}/hd/contacts/$g $ENV{HTTPHOME}/html/hd/addressbook/$g";
      }
   }

   $HDLIC = $input{'HDLIC'};
   # bind login table vars
   tie %lictab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/partners/lictab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['HDLIC', 'partner', 'IP', 'vdomain'] };

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

   if ($logo ne "") {
      $logo = adjusturl $logo;
   }


   $msg = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $msg .= "<TR BGCOLOR=0f0f5f>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff></FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Name (First, Last)</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Business Name</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Email</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Pager</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Fax</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Phone</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Bus.Phone</FONT></TD>";
   #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Directions</FONT></TD>";
   $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\" COLOR=ffffff>Edit</FONT></TD>";
   $msg .= "</TR>";
   $smsg = $msg;
   $umsg = $msg;

 
   if ($os ne "nt") {
      $execaddgroupcontact = encurl "execaddgroupcontact.cgi";
      $execshowgroupcontact = encurl "execshowgroupcontact.cgi";
      $execshowgrouppage = encurl "execshowgrouppage.cgi";
      $execshowgroupfax = encurl "execshowgroupfax.cgi";
      $execgroupcontact = encurl "execgroupcontact.cgi";
      $execprintgroupdir = encurl "execprintgroupdir.cgi";
   } else {
      $execaddgroupcontact = "execaddgroupcontact.cgi";
      $execshowgroupcontact =  "execshowgroupcontact.cgi";
      $execshowgrouppage = "execshowgrouppage.cgi";
      $execshowgroupfax = "execshowgroupfax.cgi";
      $execgroupcontact = "execgroupcontact.cgi";
      $execprintgroupdir = "execprintgroupdir.cgi";
   }
 
   #$fromstreet = replaceblanks $logtab{$login}{street};
   #$fromcity = replaceblanks $logtab{$login}{city};
   #$fromstate = replaceblanks $logtab{$login}{state};

   # bind address table vars
   system "mkdir -p $ENV{HDDATA}/listed/groups/$g/addrtab";
   system "chmod 755 $ENV{HDDATA}/listed/groups/$g/addrtab";

   tie %addrtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/groups/$g/addrtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['entryno', 'group', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'id', 'other',
        'aptno', 'busname', 'bday', 'bmonth', 'byear', 'title'] };

   $numbegin = $input{numbegin};
   $numend = $input{numend};

   $remove = $input{remove};
   hddebug "remove = $remove";
   $remove = $input{remove};
   if ($remove ne "") {
      $k = 0;
      for ($i = $numbegin; $i <= $numend; $i= $i + 1) {
          $contact = $input{"box$k"};
          $checkboxval = $input{$contact};
          #hddebug "i = $i, checkboxval = $checkboxval";
          if ($checkboxval eq "on") {
             if (exists($addrtab{$contact})) {
                delete $addrtab{$contact};
                #withdrawmoney $login;
             }
          }
          $k = $k + 1;
      }
      status("You have successfully deleted the contact. <BR>Click <a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?pnum=4&p0=$execgroupcontact&p1=biscuit&p2=jp&p3=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&g=$g&jp=$jp&rh=$rh&hs=$hs&vdomain=$vdomain&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6\">here</a> to go to contact manager.");

      if ($biscuit ne "") {
         tied(%sesstab)->sync();
         tied(%logsess)->sync();
      }
      tied(%addrtab)->sync();
      exit;
   }              
  
   $cntr = 0; 
   $letter = $input{letter};
   $letter = "\L$letter";
   $all = $input{all};
   if ($all eq "") {
     if ($letter eq "") {
        $letter = "a";
     }
   }
   if ($letter eq "") {
      $letter = "a";
   }
   $chosenletter = $letter;

   $search = $input{search};
   $searchstr = trim $input{searchstr};
   $searchstr = adjusturl $searchstr;
   $searchnum = $input{searchnum};
   hddebug "search = $search, $searchstr, $searchnum";
   $groupcontact = "groupcontact-$$";

   $cdir = "";
   ##$memnum = 0;
   $totalrecs = 0;
   foreach $mem (sort keys %addrtab) {
      $totalrecs = $totalrecs + 1;
      $fn = substr $addrtab{$mem}{fname}, 0, 1;
      $ln = substr $addrtab{$mem}{lname}, 0, 1;
      $bn = substr $addrtab{$mem}{busname}, 0, 1;
      $sn = substr $addrtab{$mem}{street}, 0, 1;

      if ($search eq "") {
	 if ($all eq "") {
            if (($letter ne "\L$fn") && ($letter ne "\L$ln")) {
               if ($letter ne "\L$bn") {
	          next;
	       }
            }
         }
     } else {
	 ## First Name OR Last Name
         if ($searchnum == 1) {
            if (( (index "\L$addrtab{$mem}{fname}", "\L$searchstr") == -1) && 
                ((index "\L$addrtab{$mem}{lname}", "\L$searchstr") == -1) ) {
               next;
             } 
         } else {
	     ## Street OR City
             if ($searchnum == 2)  {
                if ( ((index "\L$addrtab{$mem}{street}", "\L$searchstr" ) == -1)  && 
                     ((index "\L$addrtab{$mem}{city}",  "\L$searchstr") == -1) ) {
                   next;
                }
             } else {
                ## Country OR City
                if ($searchnum == 5) {
                   if ( ((index "\L$addrtab{$mem}{country}", "\L$searchstr") == -1)  && 
                        ((index "\L$addrtab{$mem}{city}", "\L$searchstr") == -1) ) {
                      next;
                   }
                } else {
                   ## "Zipcode OR State"
                   if ($searchnum == 4) {
                     if (((index "\L$addrtab{$mem}{zipcode}", "\L$searchstr") == -1)  && 
                        ((index "\L$addrtab{$mem}{state}", "\L$searchstr") == -1) ) {
                        next;
		     }
                  } else {
                     ## "City OR State"
                     if ($searchnum == 3) {
                        if ( ((index "\L$addrtab{$mem}{city}", "\L$searchstr") == -1)  && 
                             ((index "\L$addrtab{$mem}{state}", "\L$searchstr") == -1) ) {
                           next;
                        }
                     } else {
                       # "Phone OR Bus.Phone OR Cell Phone"
                       if ($searchnum == 6) {
                          if ( ((index "\L$addrtab{$mem}{phone}", "\L$searchstr") == -1)  && 
                               ((index "\L$addrtab{$mem}{bphone}", "\L$searchstr") == -1) &&
                               ((index "\L$addrtab{$mem}{cphone}", "\L$searchstr") == -1) ) {
                             next;
                          }
                       } else {
                          ## Email
                          if ($searchnum == 8) {
                             if ((index "\L$addrtab{$mem}{email}", "\L$searchstr") == -1){
                                next;
                             } 
			     
                          } else {
                             ## "Other"
                             if ($searchnum == 9) {
                                if ((index "\L$addrtab{$mem}{other}", "\L$searchstr") == -1)  {
                                   next;
                                }
                             } else {
                                ## "Title"
                                if ($searchnum == 10) {
                                   if ((index "\L$addrtab{$mem}{title}", "\L$searchstr") == -1)  {
                                      next;
                                   }
                                } else {
			           ## pager
                                   if ($searchnum == 7) {
                                      if ((index "\L$addrtab{$mem}{pager}", "\L$searchstr") == -1)  {
                                         next;
                                      }
                                   } else {
				      ## business name
                                      if ($searchnum == 11) {
                                         if ((index "\L$addrtab{$mem}{busname}", "\L$searchstr") == -1)  {
                                            next;
					 }
                                      }
				   } 
			        }
			     }
			  }
		       }
		     }
		  }
               }
            } 
         }
      }

      $cntr = $cntr +1;
      $msg = "<TR>";
      #if ($g eq "edgewater") {
         $dellink = adjusturl("execdogeneric.jsp?pnum=8&p0=$execgroupcontact&p1=biscuit&p2=ulogin&p3=jp&p4=box0&p5=$mem&p6=g&p7=remove&p8=numbegin&p9=numend&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&rh=$rh&box0=$mem&$mem=on&remove=yes&numbegin=0&numend=0&jp=$jp&g=$g&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&letter=$letter&all=");
         $msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=$dellink><IMG SRC=http://www.hotdiary.com/images/delevt.gif BORDER=0></a></FONT></TD>"; 
      #} else {
      #   $msg .= "<TD VALIGN=\"CENTER\"><FONT FACE=\"Verdana\" SIZE=\"2\"><INPUT TYPE=CHECKBOX NAME=$mem> </FONT></TD>"; 
      #}
      $cdir .= $mem;
      $cdir .= " ";

      #$memnum = $memnum + 1; 
      $memname = "$addrtab{$mem}{fname} $addrtab{$mem}{lname}";
      $size = length $memname;
      if ($size > 25) {
         $namestr = $memname;
         $memname = substr($namestr, 0, 25);
         $size = $size - 25;
         $memname .= "<BR>";
         $memname .= substr($namestr, 25, $size);
      }          
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$memname &nbsp;</FONT></TD>";
      if ($cntr == 1) {
         $searchname = $memname;
      }

      $busname = $addrtab{$mem}{busname};
      $size = length $busname;
      if ($size > 25) {
         $busstr = $busname;
         $busname = substr($busstr, 0, 25);
         $size = $size - 25;
         $busname .= "<BR>";
         $busname .= substr($busstr, 25, $size);
      }          
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$busname &nbsp;</FONT></TD>";

      $email = $addrtab{$mem}{email};
      $size = length $email;
      if ($size > 15) {
         $mail = $email;
	 $email = substr($mail, 0, 15);
	 $size = $size - 15;
	 $email .= "<BR>";
	 $email .= substr($mail, 15, $size);
      } 
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"mailto:$addrtab{$mem}{email}\">$email</a> &nbsp;</FONT></TD>";

      $dbpagertype = replaceblanks $addrtab{$mem}{pagertype};
      $dbpager = replaceblanks $addrtab{$mem}{pager};
      $uname = replaceblanks ($addrtab{$mem}{fname}. " ". $addrtab{$mem}{lname}); 
      ($dbfax = $addrtab{$mem}{'fax'}) =~ s/\n/\n<BR>/g;
      #$tostreet = replaceblanks $addrtab{$mem}{street};
      #$tocity = replaceblanks $addrtab{$mem}{city};
      #$tostate = replaceblanks $addrtab{$mem}{state};

      $pager = $dbpager;
      $to = replaceblanks($to);
      $pt = replaceblanks($pt);
      $thispage = replaceblanks($thispage);
      $thispage = "/rep/$mem/ser$title$biscuit$page_num.html";

      $pageurl = adjusturl("execdogeneric.jsp?pnum=9&p0=$execshowgrouppage&p1=biscuit&p2=thispage&p3=to&p4=pt&p5=uname&p6=dirtype&p7=jp&p8=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&thispage=$thispage&to=$dbpager&pt=$dbpagertype&uname=$uname&dirtype=$groupcontact&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&jp=$jp&g=$g");

      $size = length $pager;
      if ($size > 15) {
         $mempager = $pager;
         $pager = substr($mempager, 0, 15);
         $pager .= "<BR>"; 
         $size = $size - 15;
         $pager .= substr($mempager, 15, $size);
      }

      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$pageurl\">$pager</a>&nbsp;</FONT></TD>";

      $fax = $dbfax;
      $dbfax = getPhoneDigits $dbfax;
      $dbfax = replaceblanks($dbfax);
      $faxurl = adjusturl("execdogeneric.jsp?pnum=8&p0=$execshowgroupfax&p1=biscuit&p2=thispage&p3=to&p4=uname&p5=dirtype&p6=jp&p7=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&thispage=$thispage&to=$dbfax&uname=$uname&dirtype=$groupcontact&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&jp=$jp&g=$g"); 

      $size = length $fax;
      if ($size > 15) {
         $memfax = $fax;
         $fax = substr($memfax, 0, 15);
         $fax .= "<BR>";
         $size = $size - 15;
         $fax .= substr($memfax, 15, $size);
      }            
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$faxurl\">$fax</a>&nbsp;</FONT></TD>";

      $phone = $addrtab{$mem}{phone};
      if ($size > 15) {
         $memphone = $phone;
         $phone = substr($memphone, 0, 15);
         $phone .= "<BR>";
         $size = $size - 15;
         $phone .= substr($memphone, 15, $size);
      }          
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$phone &nbsp;</FONT></TD>";

      $bphone = $addrtab{$mem}{bphone};
      if ($size > 15) {
         $memphone = $bphone;
         $bphone = substr($memphone, 0, 15);
         $bphone .= "<BR>";
         $size = $size - 15;
         $bphone .= substr($memphone, 15, $size);
      }          
      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\">$bphone &nbsp;</FONT></TD>";
    
      #$directions = adjusturl "http://www.zip2.com/scripts/map.dll?mad1=$fromstreet&mct1=$fromcity&mst1=$fromstate&mad2=$tostreet&mct2=$tocity&mst2=$tostate&type=gis&mwt=350&mht=280&mwt1=350&mht1=280&mwt2=350&mht2=280&mwt3=350&mht3=280&method=d2d&ck=21439101&userid=55724010&userpw=xtv0J_txAwt8tE_FD0C&version=663922&sType=street&adrVer=918629102&ver=d3.0&GetDir.x=Get+Directions";
      #$msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"$directions\">Directions</a>&nbsp;</FONT></TD>";

      $moreurl = adjusturl("execdogeneric.jsp?pnum=5&p0=$execshowgroupcontact&p1=biscuit&p2=ulogin&p3=jp&p4=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=$mem&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&jp=$jp&g=$g");

      $msg .= "<TD><FONT FACE=\"Verdana\" SIZE=\"2\"><a href=\"http://$vdomain/cgi-bin/$rh/$moreurl\">Edit</a>&nbsp;</FONT></TD>"; 
 
      $msg .= "</TR>";

      if ((exists $addrtab{$mem})) {
         $smsg .= $msg;
      } else {
         $umsg .= $msg;
      }
   }

   if ($cntr > 0) {
      (@hshcdir) = split " ", $cdir; 
      $smsg .= "</TABLE>";
      $umsg .= "</TABLE>";
      #if ($g ne "edgewater") {
         #$smsg .= "<BR><BR><FONT FACE=\"Verdana\" SIZE=3><INPUT TYPE=submit NAME=remove VALUE=\"Remove\"></FONT>";
      #}
      $smsg = adjusturl $smsg;
   } else {
      $smsg = "";
   }


   $folder = "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 WIDTH=\"80%\">";
   $folder .= "<TR WIDTH=\"100%\"><TD WIDTH=\"100%\">";

   $folder .= "<TABLE BORDER=0 CELLPADDING=5 CELLSPACING=0 BGCOLOR=ee9900 WIDTH=\"100%\">";
   $folder .= "<TR ALIGN=CENTER WIDTH=\"100%\">";

   if ($search eq "Search") {
      $letter = substr $searchname, 0, 1;
      $chosenletter = $letter;
   }

   for ($i =0; $i <= 25; $i = $i + 1) {
      $letter = chr(65 + $i); 
      #hddebug "letter = $letter";
      $lt = scheduleresolve::scheduleresolve::isaddr($letter, $login, $g); 
      if ($lt == 1) {
         $letterlink = adjusturl("execdogeneric.jsp?pnum=7&p0=$execgroupcontact&p1=biscuit&p2=ulogin&p3=letter&p4=all&p5=jp&p6=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&rh=$rh&jp=$jp&g=$g&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&letter=$letter&all=");
         if ("\L$letter" eq "\L$chosenletter") {
            $bgcolor = "BGCOLOR=02994e";
         } else {
            $bgcolor = "";
         }
         if ( ("a" eq "\L$chosenletter") && ($all ne "") ) {
            $bgcolor = "";
         }
         $folder .= "<TD $bgcolor ALIGN=CENTER SIZE=1><a href=\"http://$vdomain/cgi-bin/$rh/$letterlink\"><FONT FACE=\"Verdana\" SIZE=\"2\">$letter</a></FONT></TD>";
     } else {
         $folder .= "<TD ALIGN=CENTER SIZE=1><FONT FACE=\"Verdana\" SIZE=\"2\">$letter</FONT></TD>";
     }
   }

   if ($cntr > 0) {
      $letterlink = adjusturl("execdogeneric.jsp?pnum=7&p0=$execgroupcontact&p1=biscuit&p2=ulogin&p3=letter&p4=all&p5=jp&p6=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&ulogin=&jp=$jp&g=$g&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&letter=&all=all");
      if ("$all" ne "") {
         $bgcolor = "BGCOLOR=02994e";
      } else {
         $bgcolor = "";
      }
      $folder .= "<TD $bgcolor ALIGN=CENTER SIZE=1><a href=\"http://$vdomain/cgi-bin/$rh/$letterlink\"><FONT FACE=\"Verdana\" SIZE=\"2\">All</a></FONT></TD>";
   }

   $folder .= "</TR></TABLE>";
   $folder .= "</TD></TR></TABLE>";
   $folder = adjusturl($folder);

   $status = "";
   if ($search eq "Search") {
      if ($cntr == 0) {
	 $status = "$login: No matches were found for $searchstr in your contact manager.";
      }
   }
 

      $prb = "";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "logo=$logo";
      $prb = strapp $prb, "label=$label";

      if ($os ne "nt") {
         $formenc = adjusturl "ENCTYPE=\"$ENV{HDENCODE}\"";
         $prb = strapp $prb, "formenc=$formenc";
         $execproxylogout = encurl "/proxy/execproxylogout.cgi";
         $execdeploypage =  encurl "execdeploypage.cgi";
         $execshowtopcal =  encurl "execshowtopcal.cgi";
         $execgroupcontact = encurl "execgroupcontact.cgi";
      } else {
         $prb = strapp $prb, "formenc=";
         $execproxylogout =  "/proxy/execproxylogout.cgi";
         $execdeploypage =  "execdeploypage.cgi";
         $execshowtopcal =  "execshowtopcal.cgi";
         $execgroupcontact = "execgroupcontact.cgi";
      }

      if ($jp ne "") {
         if (-f "$ENV{HDDATA}/$alpha/$jp/templates/groupcontact.html") {
	    $tmpl = "$ENV{HDDATA}/$alpha/$jp/templates/groupcontact.html";
	 } else {
	     $tmpl = "$ENV{HDTMPL}/groupcontact.html";
	 }
      } else {
	 $tmpl = "$ENV{HDTMPL}/groupcontact.html";
      }

      $prb = strapp $prb, "template=$tmpl";
      $prb = strapp $prb, "templateout=$ENV{HDHOME}/tmp/$g-$$.html";

      $prb = strapp $prb, "biscuit=$biscuit";
      $welcome = "Welcome";
      $prb = strapp $prb, "welcome=$welcome";
      $prb = strapp $prb, "g=$g";
      $prb = strapp $prb, "login=$login";
      $prb = strapp $prb, "HDLIC=$HDLIC";
      $prb = strapp $prb, "ip=$ip";
      $prb = strapp $prb, "rh=$rh";
      $prb = strapp $prb, "hs=$hs";
      $prb = strapp $prb, "vdomain=$vdomain";
      $hiddenvars = "<INPUT TYPE=HIDDEN NAME=p0 VALUE=\"$execgroupcontact\">";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p1 VALUE=biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p2 VALUE=numbegin>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p3 VALUE=numend>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p4 VALUE=jp>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p5 VALUE=remove>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p6 VALUE=search>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p7 VALUE=searchnum>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p8 VALUE=searchstr>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p9 VALUE=g>";

      #values of checkboxes as each parameter
      $k = 0;
      $mcntr = 10;
      $numend = $mcntr;
      $numbegin = $mcntr;

      # this tells from where the parameter for selection starts
      #foreach $cn (@hshcdir) {
      #   $cn = trim $cn;
      #	  $numend = $numend + 1;
      #   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=box$k>";
      #	  $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=box$k VALUE=$cn>";
      #   $mcntr = $mcntr + 1;
      #   $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=p$mcntr VALUE=$cn>";
      #   $mcntr = $mcntr + 1;
      #   $k = $k + 1;
      #}
      $numend = $numend - 1;

      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=pnum VALUE=$mcntr>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=biscuit VALUE=$biscuit>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=g VALUE=$g>";
      $hiddenvars .= "<INPUT TYPE=HIDDEN NAME=jp VALUE=$jp>";
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
      $prb = strapp $prb, "bizdir=$smsg";
      $prb = strapp $prb, "letter=$folder";
      $prb = strapp $prb, "jp=$jp";
      $prb = strapp $prb, "cntr=$totalrecs contacts";


   $prb = strapp $prb, "status=$status";
   $bizlabel = "$login $fname $lname - Address Book";
   $prb = strapp $prb, "bizlabel=$bizlabel";
   $prb = strapp $prb, "execproxylogout=$execproxylogout";
   $prb = strapp $prb, "execdeploypage=$execdeploypage";
   $prb = strapp $prb, "execshowtopcal=$execshowtopcal";
   $prb = strapp $prb, "execaddgroupcontact=$execaddgroupcontact";
   $prb = strapp $prb, "execprintgroupdir=$execprintgroupdir";
   $prb = strapp $prb, "g=$g";

   if ($biscuit eq "") {
      $prb = strapp $prb, "logout=";
      $prb = strapp $prb, "home=";
      $prb = strapp $prb, "new=";
      $prb = strapp $prb, "features=";
      $prb = strapp $prb, "help=";
   } else {
      $prb = strapp $prb, "logout=Logout";
      $prb = strapp $prb, "home=Home";
      $prb = strapp $prb, "new=What's New";
      $prb = strapp $prb, "features=Features";
      $prb = strapp $prb, "help=Help";
   }

   #if ( ($login eq "mjoshi") || ($login eq "smitha") ) {
      $printcontact = adjusturl ("<a href=\"http://$vdomain/cgi-bin/$rh/execdogeneric.jsp?pnum=4&p0=$execprintgroupdir&p1=biscuit&p2=jp&p3=g&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&HDLIC=$HDLIC&biscuit=$biscuit&g=$g&jp=$jp&rh=$rh&vdomain=$vdomain&hs=$hs&le4=os&re4=os&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6&letter=&all=all\">Print Report</a>");
   #} else {
   #     $printcontact = "";
   #}
   $prb = strapp $prb, "printcontact=$printcontact";

   parseIt $prb;

   system "cat $ENV{HDTMPL}/content.html";
   system "cat $ENV{HDHOME}/tmp/$g-$$.html";
  


   if ($biscuit ne "") {
      tied(%sesstab)->sync();
      tied(%logsess)->sync();
   }

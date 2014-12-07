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
# FileName: updatemgcal.cgi
# Purpose: New HotDiary Update merged Group Calendar
# Creation Date: 06-14-99
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

$hddomain = $ENV{HDDOMAIN};
$hddomain80 = $ENV{HDDOMAIN80};
$hotdiary = $ENV{HOTDIARY};
$diary = $ENV{DIARY};

   #print &PrintHeader;
   #print &HtmlTop ("calclient.cgi example");

   $hdcookie = $input{HTTP_COOKIE};
   $login = getlogin($hdcookie);

   $vdomain = trim $input{'vdomain'};
   if ($vdomain eq "") {
      $vdomain = "$hotdiary";
   } 
   $os = $input{'os'};
   $hs = $input{'hs'};
   $jp = $input{'jp'};
   if ( ("1800calendar.com" eq "\L$vdomain") || ("www.1800calendar.com" eq "\L$vdomain") ) {
      $icgi = "index.cgi?jp=$jp";
   } else {
      $icgi = adjusturl "index.html";
   }

   $biscuit = $input{'biscuit'};
   if ($biscuit eq "") {
      status("Your login session information is missing. Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
       'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish', 'referer'] };

   # check if session record exists.
   if (!exists $sesstab{$biscuit}) {
      status("Invalid session or session does not exists. Please relogin.  Click <a href=\"http://$vdomain/$icgi\" TARGET=\"_parent\"> here</a> to login.\n");
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
      status("$login: Your session has already timed out. However, all your personal data is completely intact. Click <a href=\"http://$vdomain/$icgi\" target=\"_parent\"> here</a> to login again.");
      exit;
   }
   $alph = substr $login, 0, 1;
   $alph = $alph . '-index';


   tie %hdtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/hdtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['title', 'logo' ] };

   if (exists $hdtab{$login}) {
      $p2 = adjusturl($hdtab{$login}{title});
   } else {
      $p2 = "HotDiary";
   }
                           
   # bind mmergtab table vars
   tie %mmergtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/mmergtab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 
                 'listed', 'readonly', 'groups', 'logins'] };

   # bind lmergetab table vars
   tie %lmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/listed/lmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle',
                  'groupdesc', 'password', 'ctype', 'cpublish', 'corg', 
                 'listed', 'groups', 'logins'] };

# bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec', 
   SCHEMA => { 
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone','email', 'url', 'checkid', 'winner', 
        'remoteaddr', 'informme', 'cserver', 'zone', 'calpublish',
        'referer'] };      


   $calname = trim $input{'calname'};

   if ( (exists($mmergtab{$calname})) || 
       (exists($lmergetab{$calname})) || 
       (exists($logtab{$calname})) ) {
       status("$login: Please choose another name. A group  $calname already exists.");
       exit;
   }

   $ctype = $input{'ctype'};
   $caltitle = trim $input{'caltitle'};
   $corg = trim $input{'corg'};
   $listed = trim $input{'listed'};
   hddebug "listed = $listed";
   $readonly = $input{'readonly'};
   if ($caltitle eq "") {
      status("$login: Calendar title is empty. Please specify a calendar title.");
      exit;
   }
   if (notDesc $caltitle) {
      status("$login: Invalid characters in calendar title.");
      exit;
   }

   #if ($corg eq "") {
   #   status("$login: Organization/Company Name of Calendar is empty. Please specify a Organization/Company Name");
   #   exit;
   #}

   if (notDesc $corg) {
      status("$login: Invalid characters in Organization/Company Name of Calendar.");
      exit;
   }


   $calpassword = trim $input{'calpassword'};
   $calpassword = "\L$calpassword";
   if (notDesc $calpassword) {
      status("$login: Invalid characters in calendar password.");
      exit;
   }

   $calrpassword = trim $input{'calrpassword'};
   $calrpassword = "\L$calrpassword";
   if (notDesc $calrpassword) {
      status("$login: Invalid characters in calendar repeat password.");
      exit;
   }

   if ($calpassword ne $calrpassword) {
      status("$login: Calendar password field and the repeat password field do not match. Please use the Back button and enter identical passwords.");
      exit;
   }
 
   #$invitemsg = "";

 
   $contact = $input{'contact'};
   hddebug "contact = $contact";
   if ($contact ne "") {
      $eventdetails .= "Calendar Master Name:  $logtab{$login}{fname} $logtab{$login}{lname}\n"; 
      $eventdetails .= "Calendar Id: $calname \n";
      $eventdetails .= "Calendar Title: $caltitle \n";
      $eventdetails .= "Calendar Type: $ctype \n";
      $eventdetails .= "Organization Company/Name: $corg \n"; 
      $eventdetails .= "Calendar Password:  $calpassword \n"; 
   }

   $mname = $login;
   (@hshemail) = split ",", $contact;
   $cntr = 0;
   hddebug "email = $#hshemail";

   # bind surveytab table vars
   tie %surveytab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/surveytab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login', 'hearaboutus', 'browser', 'rhost', 'calinvite',
		'installation', 'domains', 'domain', 'orgrole', 'organization', 
		'orgsize', 'budget', 'timeframe', 'platform', 'priority', 
		'editcal', 'calpeople'] };

   foreach $cn (@hshemail) {
       $cntr = $cntr + 1;
       $cn = "\L$cn";
       $cn = trim $cn;
       hddebug "cn = $cn";
       hddebug "mname = $mname";
       if ("\L$logtab{$mname}{email}" eq $cn) {
          next;
       }

       if ($cn eq "") {
          next;
       }

       if (exists ($logtab{$cn} ) ) {
          if ($surveytab{$cn}{calinvite} ne "CHECKED") {
             #$invitemsg .= "<BR><FONT COLOR=ff0000>$cn specified in your invitation list prefers not to receive invitations from others.</FONT>";
             #hddebug "invitemsg = $invitemsg";
             next;
          }
          $login_db = $cn;
          $cn = $logtab{$cn}{email};
          $eemail = 1;
          $oldlogin = $login_db;
          hddebug "oldlogin = $login_db";
       } else {
          ($login_db, $domain) = split '@', $cn;
          $login_db = trim $login_db;
          $eemail = 0;
       }

       hddebug "login_db = $login_db"; 
       if ($login_db =~ /\&/) {
          next;
       }
       #if ( (!(notLogin $login_db)) || (exists ($logtab{$login_db} )) ) {
       if ( (notLogin $login_db) || (exists ($logtab{$login_db} )) ) {
          if ($eemail ne "1") {
             $oldlogin = $login_db;
             if (exists($logtab{$login_db} )) {
                $login_db = "l$login_db$$-$cntr";
             }
             hddebug "login = $login_db";
          }
       }
       #if (!exists ($logtab{$login_db} )) {
       hddebug "login does notexist = $login_db eemail =$eemail"; 
          if ($eemail ne "1") {
             $logtab{$login_db}{'login'} = $login_db;
             $logtab{$login_db}{'fname'} = $login_db;
             $logtab{$login_db}{'password'} = $login_db;
             $logtab{$login_db}{'email'} = $cn;
             $surveytab{$login_db}{'login'} = $login_db;
             $surveytab{$login_db}{'hearaboutus'} = "Friend";
             $surveytab{$login_db}{'browser'} = $ENV{'HTTP_USER_AGENT'};
             tied(%surveytab)->sync();
          }


       hddebug "oldlogin = $oldlogin";
       if (!exists $logtab{$oldlogin}) {
          next;
       }
       $emsg = "Dear $logtab{$oldlogin}{fname}, \n \n";
       $uname = $logtab{$mname}{'fname'} . " " . $logtab{$mname}{'lname'};
       $emsg .= "You have been invited by $uname to join calendar group.\n\n";
       $emsg .= "Calendar Details: \n";
       $emsg .=  $eventdetails;
       $emsg .=  "\n\n";
       $emsg .= "If you would like to contact $uname directly, please send an email to $uname at $logtab{$mname}{'email'}. $uname's member login ID on HotDiary is \"$mname\".\n";

       if ($eemail ne "1") {
          $emsg .= "\nName: $logtab{$login_db}{'fname'} $logtab{$login_db}{'lname'}\n";
          $emsg .= "Login: $login_db \n";
          $emsg .= "Password: $logtab{$login_db}{'password'}\n\n";
          $emsg .= qx{cat $ENV{'HDHOME'}/letters/reginvitation};
       }

       $emsg .= "\n\nRegards,\nHotDiary Inc.\n\n";
       $emsg .= "HotDiary ($hddomain80) - New Generation Calendaring Products and Services\n";

       qx{echo \"$emsg\" > $ENV{HDHOME}/tmp/reginviteletter$$};
       $logtab{$login_db}{email} = trim $logtab{$login_db}{email};
       if ($logtab{$login_db}{email} =~ /\s/) {
          status "Found spaces in email addresses ($logtab{$login_db}{email}). Please separate email addresses with a comma.";
          exit;
       }
       if (notEmailAddress $logtab{$login_db}{email}) {
          status "Invalid format in email address ($logtab{$login_db}{email}). Please specify correct email address.";
          exit;
       }
       qx{/bin/mail -s \"Invitation From $uname\" $logtab{$login_db}{email} < $ENV{HDHOME}/tmp/reginviteletter$$};
       system "$ENV{HDEXECCGI}/execcleanproducts $ENV{HDHOME}/tmp/reginviteletter$$ 1200";

       $alphdb = substr $login_db, 0, 1;
       $alphdb = $alphdb . '-index';
       if ($eemail ne "1") {
           system "/bin/mkdir -p $ENV{HDREP}/$alphdb/$login_db";
           system "/bin/chmod 755 $ENV{HDREP}/$alphdb/$login_db";
           system "/bin/mkdir -p $ENV{HDHOME}/rep/$alphdb/$login_db";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphdb/$login_db";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphdb/$login_db";
           system "/bin/touch $ENV{HDDATA}/$alphdb/$login_db/addrentrytab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphdb/$login_db/addrentrytab";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphdb/$login_db/addrtab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphdb/$login_db/addrtab";
           system "/bin/touch $ENV{HDDATA}/$alphdb/$login_db/apptentrytab";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphdb/$login_db/apptentrytab";
           system "/bin/mkdir -p $ENV{HDDATA}/$alphdb/$login_db/appttab";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphdb/$login_db/appttab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphdb/$login_db/personal/pgrouptab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphdb/$login_db/subscribed/smergetab";
           system "/bin/mkdir -p $ENV{HDDATA}/groups/$alphdb/$login_db/founded/fmergetab";
           system "/bin/chmod -R 775 $ENV{HDDATA}/groups/$alphdb/$login_db";
           system "/bin/cp $ENV{HDTMPL}/index.html $ENV{HDREP}/$alphdb/$login_db/index.html";
           system "/bin/cp $ENV{HDHOME}/calendar/calendar_events.txt $ENV{HDDATA}/$alphdb/$login_db";
           system "/bin/chmod 775 $ENV{HDDATA}/$alphdb/$login_db/calendar_events.txt";

           system "/bin/mkdir -p $ENV{HDDATA}/$alphdb/$login_db/faxtab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphdb/$login_db/faxtab";

           system "/bin/mkdir -p $ENV{HDDATA}/$alphdb/$login_db/faxdeptab";
           system "/bin/chmod 755 $ENV{HDDATA}/$alphdb/$login_db/faxdeptab";
        }
        tie %smergetab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/groups/$alphdb/$login_db/subscribed/smergetab",
        SUFIX => '.rec',
        SCHEMA => {
           ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc' , 'password', 'ctype', 'cpublish', 'corg' ] };
        if (!(exists $smergetab{$calname})) {
     hddebug "calname $calname does not exist in $login_db subscribed";
           $smergetab{$calname}{'groupname'} = $calname;
           $smergetab{$calname}{'groupfounder'} = $mmergtab{$calname}{'groupfounder'};
           $smergetab{$calname}{'grouptype'} = $mmergtab{$calname}{'grouptype'};
           $smergetab{$calname}{'grouptitle'} = $mmergtab{$calname}{'grouptitle'};
           $smergetab{$calname}{'groupdesc'} = $mmergtab{$calname}{'groupdesc'};
           $smergetab{$calname}{'password'} = $mmergtab{$calname}{'password'};
           $smergetab{$calname}{'ctype'} = $mmergtab{$calname}{'ctype'};
           $smergetab{$calname}{'cpublish'} = $mmergtab{$calname}{'cpublish'};
           tied(%smergetab)->sync();

           system "/bin/mkdir -p $ENV{HDDATA}/listed/merged/$calname/usertab";
           system "/bin/chmod 755 $ENV{HDDATA}/listed/merged/$calname/usertab";
           tie %usertab, 'AsciiDB::TagFile',
           DIRECTORY => "$ENV{HDDATA}/listed/merged/$calname/usertab",
           SUFIX => '.rec',
           SCHEMA => {
           ORDER => ['login'] };
           $usertab{$login_db}{'login'} = $login_db;
           tied(%usertab)->sync();
        }
    }



   $cdesc = $input{'cdesc'};
   if (notDesc $cdesc eq "") {
      status("$login: Invalid characters in calendar description.");
      exit;
   }

   # bind founded group table vars
   tie %fmergetab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/merged/$alph/$login/founded/fmergetab",
   SUFIX => '.rec',
   SCHEMA => {
        ORDER => ['groupname', 'groupfounder', 'grouptype', 'grouptitle', 'groupdesc', 'password', 'ctype', 'cpublish', 'corg' ] };


   $mmergtab{$calname}{'grouptitle'} = $caltitle;
   $mmergtab{$calname}{'groupdesc'} = $cdesc;
   $mmergtab{$calname}{'password'} = $calpassword;
   $mmergtab{$calname}{'ctype'} = $ctype;
   $mmergtab{$calname}{'corg'} = $corg;
   $mmergtab{$calname}{'listed'} = $listed;
   $mmergtab{$calname}{'readonly'} = $readonly;

   $fmergetab{$calname}{'grouptitle'} = $caltitle;
   $fmergetab{$calname}{'groupdesc'} = $cdesc;
   $fmergetab{$calname}{'password'} = $calpassword;
   $fmergetab{$calname}{'ctype'} = $ctype;
   $fmergetab{$calname}{'corg'} = $corg;

   $cpublish = $input{'cpublish'};
   $mmergtab{$calname}{'cpublish'} = $cpublish;
   if ($cpublish eq "on") {
      $logtab{$login}{referer} = $jp;
      tied(%logtab)->sync();
      if (!(-d "$ENV{HTTPHOME}/html/hd/merged/$calname"))  {
         system "mkdir -p $ENV{HTTPHOME}/html/hd/merged/$calname";
         if ($hs eq "") {
             $cmsg = "<p>$p2 has created a password-protected website for you at <a href=\"http://$vdomain/merged/$calname\">http://$vdomain/merged/$calname</a>.";
         } else {
             $cmsg = "<p>$p2 has created a password-protected website for you at <a href=\"http://$vdomain/$hs/merged/$calname\">http://$vdomain/$hs/merged/$calname</a>.";
         }
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/merged/$calname/index.cgi")) {
         system "ln -s $ENV{HDCGI}/merged/index.cgi $ENV{HTTPHOME}/html/hd/merged/$calname";
      }
      if (!(-f "$ENV{HTTPHOME}/html/hd/merged/$calname/mergedwebpage.cgi")) {
         system "ln -s $ENV{HDCGI}/merged/mergedwebpage.cgi $ENV{HTTPHOME}/html/hd/merged/$calname";
      }
   } else {
      if (-d "$ENV{HTTPHOME}/html/hd/merged/$calname")  {
         if ($calname ne "") {
            if (-f "$ENV{HTTPHOME}/html/hd/merged/$calname/index.cgi") {
                system "rm -f $ENV{HTTPHOME}/html/hd/merged/$calname/index.cgi";
            }
         }
         if ($calname ne "") {
           if (-f "$ENV{HTTPHOME}/html/hd/merged/$calname/mergedwebpage.cgi") {
              system "rm -f $ENV{HTTPHOME}/html/hd/merged/$calname/mergedwebpage.cgi";
           }
         }
         if ($calname ne "") {
            if (-d "$ENV{HTTPHOME}/html/hd/merged/$calname")  {
               system "rmdir $ENV{HTTPHOME}/html/hd/merged/$calname";
               $cmsg = "<p>$p2 has removed your  website for you.";
            }
         } 
      }
   }

   $rh = $input{'rh'};

   $prml = "";
   #hddebug "invitemsg2 = $invitemsg";
   #$invitemsg = goodwebstr $invitemsg;
   $msg = "$login: $calname updated. Password is $calpassword"; 
   $msg = replacewithplus($msg);
   $prml = strapp $prml, "template=$ENV{HDTMPL}/redirect_url.html";
   $prml = strapp $prml, "templateout=$ENV{HDREP}/$alph/$login/mgc-$biscuit-$$.html";
   $prml = strapp $prml, "login=$login";

   if ($rh eq "") {
      $cgi = adjusturl "/cgi-bin/execmgcal.cgi?biscuit=$biscuit&jp=$jp&os=$os"; 
   } else {
      $cgi = adjusturl "/cgi-bin/$rh/execmgcal.cgi?biscuit=$biscuit&jp=$jp&os=$os"; 
   }

   $searchcal = adjusturl "$cgi&f=sgc";
   $prml = strapp $prml, "logo=";
   $prml = strapp $prml, "searchcal=$searchcal"; 
   $createcal = adjusturl "$cgi&f=cpc";
   $prml = strapp $prml, "createcal=$createcal";  
   $prml = strapp $prml, "welcome=Welcome";
   if ($rh eq "") {
      $cgis = adjusturl "/cgi-bin/execmgcal.cgi?biscuit=$biscuit&jp=$jp&os=$os";
   } else {
      $cgis = adjusturl "/cgi-bin/$rh/execmgcal.cgi?biscuit=$biscuit&jp=$jp&os=$os";
   }

   $prml = strapp $prml, "home=$cgis"; 
   $pgroups = $input{'pgroups'};

   #if (-f "$ENV{HDREP}/$alph/$login/topcal.html") {
   #   $pcgi = adjusturl "/cgi-bin/$rh/execdogeneric.cgi?p0=ZXhlY3Nob3d0b3BjYWwuY2dp&p1=biscuit&pnum=3&re0=CGISUBDIR&le0=rh&re1=HTTPSUBDIR&le1=hs&re2=SERVER_NAME&le2=vdomain&re3=HDLIC&le3=HDLIC&le4=os&re4=os&biscuit=$biscuit&re5=HTTP_COOKIE&le5=HTTP_COOKIE&enum=6";
   #} else {
      if ($rh eq "") {
         $pcgi = adjusturl "/cgi-bin/execmgcal.cgi?biscuit=$biscuit&f=mc&status=$msg&jp=$jp&os=$os";
      } else {
         $pcgi = adjusturl "/cgi-bin/$rh/execmgcal.cgi?biscuit=$biscuit&f=mc&status=$msg&jp=$jp&rh=$rh&os=$os";
      }
   #}

   $prml = strapp $prml, "redirecturl=$pcgi";
   parseIt $prml;
   system "/bin/cat $ENV{HDTMPL}/content.html";
   system "/bin/cat $ENV{HDREP}/$alph/$login/mgc-$biscuit-$$.html";

   # reset the timer.
   $sesstab{$biscuit}{'time'} = time();

   tied(%sesstab)->sync();
   tied(%logsess)->sync();


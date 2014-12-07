package tp::tp;
use Exporter;

require Exporter;

@ISA = qw(Exporter);
@EXPORT = qw(replaceit strapp parseIt );

sub replaceit {
  my($line, $name, $data) = @_;
  $eline = $line;
  $eline =~ s/\:$name\:/$data/g;
  return $eline;
}

# this is the old one used before oct 6th
#
#sub replaceit {
#  my($line, $name, $data) = @_;
#  #print $line, $name, $data;
#  $eline = "$line";
#  if ($line=~/$name/) {
#     ($prefix, $var, $postfix)=split(/:/);
#     $eline = sprintf "%s%s%s\n", $prefix, $data, $postfix;
#  }
#  return $eline;
#}

sub strapp {
  my($prml, $prm) = @_;
  $prm =~ s/\?/___/g;
  return "$prml\?$prm";
}

sub parseIt {
  my($args) = @_;
  (@hashargs) = split("\\?", $args);

  #print "args = ", $hashargs[0], "\n";
  #print "args = ", $hashargs[1], "\n";

  #%arglist = ();   # may want to init this in distant future
  # currently, arglist is behaving like a global var even though
  # it is declared locally in this function. so it's hash elements
  # are remembered across calls to this function.
  foreach $i (@hashargs) {
     (@onearg) = split("\=", $i);
     $arglist{$onearg[0]} = $onearg[1];
     $arglist{$onearg[0]} =~ s/___/\?/g;
     $arglist{$onearg[0]} =~ s/\-\-\-/\=/g;
     #print "oneargp[0] = ", $onearg[0], "\n";
     #print "oneargp[1] = ", $onearg[1], "\n";
  }

 # foreach $i (keys %arglist) {
 #    print "$i = ", $arglist{$i}, "\n";
 # }

  open infiile, "<$arglist{'template'}";
  #print "infiile = ", $arglist{'template'}, "\n";
  if ($arglist{'templateout'} ne "") {
     open outfiile, ">$arglist{'templateout'}";
  }
  #print "outfiile = ", $arglist{'templateout'}, "\n";
  #print "expiry = $arglist{'expiry'}\n";
  while (<infiile>) {
     chop;
     $line = $_;
     $eline = $line;
     $eline = replaceit $eline, '\$login', $arglist{'login'};
     $eline = replaceit $eline, '\$biscuit', $arglist{'biscuit'};
     $eline = replaceit $eline, '\$nextpage', $arglist{'nextpage'};
     $eline = replaceit $eline, '\$prevpage', $arglist{'prevpage'};
     $eline = replaceit $eline, '\$password', $arglist{'password'};
     $eline = replaceit $eline, '\$rpassword', $arglist{'rpassword'};
     $eline = replaceit $eline, '\$label', $arglist{'label'};
     $eline = replaceit $eline, '\$actioncgi', $arglist{'actioncgi'};
     $eline = replaceit $eline, '\$checkboxfield', $arglist{'checkboxfield'};
     $eline = replaceit $eline, '\$entryno', $arglist{'entryno'};
     $eline = replaceit $eline, '\$entrynfield', $arglist{'entrynfield'};
     $eline = replaceit $eline, '\$numentries', $arglist{'numentries'};
     $eline = replaceit $eline, '\$fname', $arglist{'fname'};
     $eline = replaceit $eline, '\$fnamfield', $arglist{'fnamfield'};
     $eline = replaceit $eline, '\$lname', $arglist{'lname'};
     $eline = replaceit $eline, '\$lnamfield', $arglist{'lnamfield'};
     $eline = replaceit $eline, '\$street', $arglist{'street'};
     $eline = replaceit $eline, '\$streefield', $arglist{'streefield'};
     $eline = replaceit $eline, '\$city', $arglist{'city'};
     $eline = replaceit $eline, '\$citfield', $arglist{'citfield'};
     $eline = replaceit $eline, '\$state', $arglist{'state'};
     $eline = replaceit $eline, '\$statfield', $arglist{'statfield'};
     $eline = replaceit $eline, '\$zipcode', $arglist{'zipcode'};
     $eline = replaceit $eline, '\$zipcodfield', $arglist{'zipcodfield'};
     $eline = replaceit $eline, '\$country', $arglist{'country'};
     $eline = replaceit $eline, '\$countrfield', $arglist{'countrfield'};
     $eline = replaceit $eline, '\$pager', $arglist{'pager'};
     $eline = replaceit $eline, '\$pagefield', $arglist{'pagefield'};
     $eline = replaceit $eline, '\$phone', $arglist{'phone'};
     $eline = replaceit $eline, '\$phonfield', $arglist{'phonfield'};
     $eline = replaceit $eline, '\$fax', $arglist{'fax'};
     $eline = replaceit $eline, '\$fafield', $arglist{'fafield'};
     $eline = replaceit $eline, '\$cellp', $arglist{'cellp'};
     $eline = replaceit $eline, '\$cphonfield', $arglist{'cphonfield'};
     $eline = replaceit $eline, '\$busp', $arglist{'busp'};
     $eline = replaceit $eline, '\$bphonfield', $arglist{'bphonfield'};
     $eline = replaceit $eline, '\$email', $arglist{'email'};
     $eline = replaceit $eline, '\$emaifield', $arglist{'emaifield'};
     $eline = replaceit $eline, '\$url', $arglist{'url'};
     $eline = replaceit $eline, '\$urfield', $arglist{'urfield'};
     $eline = replaceit $eline, '\$month', $arglist{'month'};
     $eline = replaceit $eline, '\$montfield', $arglist{'montfield'};
     $eline = replaceit $eline, '\$day', $arglist{'day'};
     $eline = replaceit $eline, '\$dafield', $arglist{'dafield'};
     $eline = replaceit $eline, '\$year', $arglist{'year'};
     $eline = replaceit $eline, '\$yeafield', $arglist{'yeafield'};
     $eline = replaceit $eline, '\$hour', $arglist{'hour'};
     $eline = replaceit $eline, '\$houfield', $arglist{'houfield'};
     $eline = replaceit $eline, '\$min', $arglist{'min'};
     $eline = replaceit $eline, '\$mifield', $arglist{'mifield'};
     $eline = replaceit $eline, '\$sec', $arglist{'sec'};
     $eline = replaceit $eline, '\$sefield', $arglist{'sefield'};
     $eline = replaceit $eline, '\$meridian', $arglist{'meridian'};
     $eline = replaceit $eline, '\$meridiafield', $arglist{'meridiafield'};
     $eline = replaceit $eline, '\$dhour', $arglist{'dhour'};
     $eline = replaceit $eline, '\$dhoufield', $arglist{'dhoufield'};
     $eline = replaceit $eline, '\$dmin', $arglist{'dmin'};
     $eline = replaceit $eline, '\$dmifield', $arglist{'dmifield'};
     $eline = replaceit $eline, '\$dtype', $arglist{'dtype'};
     $eline = replaceit $eline, '\$dtypfield', $arglist{'dtypfield'};
     $eline = replaceit $eline, '\$atype', $arglist{'atype'};
     $eline = replaceit $eline, '\$atypfield', $arglist{'atypfield'};
     $eline = replaceit $eline, '\$subject', $arglist{'subject'};
     $eline = replaceit $eline, '\$subjecfield', $arglist{'subjecfield'};
     $eline = replaceit $eline, '\$desc', $arglist{'desc'};
     $eline = replaceit $eline, '\$desfield', $arglist{'desfield'};
     $eline = replaceit $eline, '\$distribution', $arglist{'distribution'};
     $eline = replaceit $eline, '\$distributiofield', $arglist{'distributiofield'};
     $eline = replaceit $eline, '\$colledit', $arglist{'colledit'};
     $eline = replaceit $eline, '\$colledifield', $arglist{'colledifield'};
     $eline = replaceit $eline, '\$leftFrame', $arglist{'leftFrame'};
     $eline = replaceit $eline, '\$rightFrame', $arglist{'rightFrame'};
     $eline = replaceit $eline, '\$expiry', $arglist{'expiry'};
     $eline = replaceit $eline, '\$redirecturl', $arglist{'redirecturl'};
     $eline = replaceit $eline, '\$checkid', $arglist{'checkid'};
     $eline = replaceit $eline, '\$mname', $arglist{'mname'};
     $eline = replaceit $eline, '\$mnamfield', $arglist{'mnamfield'};
     $eline = replaceit $eline, '\$memolist', $arglist{'memolist'};
     $eline = replaceit $eline, '\$thispage', $arglist{'thispage'};
     $eline = replaceit $eline, '\$from', $arglist{'from'};
     $eline = replaceit $eline, '\$to', $arglist{'to'};
     $eline = replaceit $eline, '\$pageurl', $arglist{'pageurl'}; 
     $eline = replaceit $eline, '\$jumpurl', $arglist{'jumpurl'}; 
     $eline = replaceit $eline, '\$zone', $arglist{'zone'};
     $eline = replaceit $eline, '\$zonfield', $arglist{'zonfield'};
     $eline = replaceit $eline, '\$zonestr', $arglist{'zonestr'};
     $eline = replaceit $eline, '\$zonstrfield', $arglist{'zonstrfield'};
     $eline = replaceit $eline, '\$monthnum', $arglist{'monthnum'};
     $eline = replaceit $eline, '\$montnumfield', $arglist{'montnumfield'};
     $eline = replaceit $eline, '\$pagenumber', $arglist{'pagenumber'};
     $eline = replaceit $eline, '\$label1', $arglist{'label1'};
     $eline = replaceit $eline, '\$label2', $arglist{'label2'};
     $eline = replaceit $eline, '\$faxurl', $arglist{'faxurl'}; 
     $eline = replaceit $eline, '\$directions', $arglist{'directions'}; 
     $eline = replaceit $eline, '\$groupname', $arglist{'groupname'}; 
     $eline = replaceit $eline, '\$groupfounder', $arglist{'groupfounder'}; 
     $eline = replaceit $eline, '\$grouptype', $arglist{'grouptype'}; 
     $eline = replaceit $eline, '\$grouptitle', $arglist{'grouptitle'}; 
     $eline = replaceit $eline, '\$groupdesc', $arglist{'groupdesc'}; 
     $eline = replaceit $eline, '\$grouptypefield', $arglist{'grouptypefield'}; 
     $eline = replaceit $eline, '\$groupnamefield', $arglist{'groupnamefield'}; 
     $eline = replaceit $eline, '\$pgroups', $arglist{'pgroups'}; 
     $eline = replaceit $eline, '\$groupmemberfield', $arglist{'groupmemberfield'}; 
     $eline = replaceit $eline, '\$groupmember', $arglist{'groupmember'}; 
     $eline = replaceit $eline, '\$distopt', $arglist{'distopt'}; 
     $eline = replaceit $eline, '\$calendarprog', $arglist{'calendarprog'}; 
     $eline = replaceit $eline, '\$buddy', $arglist{'buddy'};
     $eline = replaceit $eline, '\$radiovalue', $arglist{'radiovalue'};
     $eline = replaceit $eline, '\$radiocheck', $arglist{'radiocheck'};
     $eline = replaceit $eline, '\$pagertype', $arglist{'pagertype'};
     $eline = replaceit $eline, '\$pagertypfield', $arglist{'pagertypfield'};
     $eline = replaceit $eline, '\$logaccount', $arglist{'logaccount'};
     $eline = replaceit $eline, '\$logaccounfield', $arglist{'logaccounfield'};
     $eline = replaceit $eline, '\$recurtype', $arglist{'recurtype'};
     $eline = replaceit $eline, '\$recurtypfield', $arglist{'recurtypfield'};
     $eline = replaceit $eline, '\$otherinfo', $arglist{'otherinfo'};
     $eline = replaceit $eline, '\$otherinffield', $arglist{'otherinffield'};
     $eline = replaceit $eline, '\$aptno', $arglist{'aptno'};
     $eline = replaceit $eline, '\$aptnfield', $arglist{'aptnfield'};
     $eline = replaceit $eline, '\$busname', $arglist{'busname'};
     $eline = replaceit $eline, '\$busnamfield', $arglist{'busnamfield'};
     $eline = replaceit $eline, '\$bmonth', $arglist{'bmonth'};
     $eline = replaceit $eline, '\$bmontfield', $arglist{'bmontfield'};
     $eline = replaceit $eline, '\$byear', $arglist{'byear'};
     $eline = replaceit $eline, '\$byeafield', $arglist{'byeafield'};
     $eline = replaceit $eline, '\$bday', $arglist{'bday'};
     $eline = replaceit $eline, '\$bdafield', $arglist{'bdafield'};
     if ($arglist{'templateout'} ne "") {
        print outfiile "$eline\n";
     } else {
        print "$eline\n";
     }
  }
  close outfiile;
  return 0;
}

1;

__END__

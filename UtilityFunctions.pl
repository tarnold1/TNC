#*******************************************************************************
#   Module name         : UtilityFunctions.pl
#   Main program module : 
#   Purpose             : Collection of generic functions/procedures used by Perl conversion tools.
#   History             :
#       040227  wmk  Original coding.
#
#*******************************************************************************

%CustomerLUT = ('mchp', 'Microchip',                            # Customer LUT
                'hisi', 'HiSilicon',
                'pere', 'pSemi',                                # formerly Peregrine Semiconductor
                );

# -------------------------------------------------------------------------
sub hashDump {
    local () = @_;

    foreach $Element (sort keys (%ObjectTypeLUT)) {


    }
    $break = 1;
}

# -------------------------------------------------------------------------
sub create_enVisionRev {
    local($enVisionRev) = @_;
    $enVisionRev =~ /R(\d+).(\d+).?(\d*).?(\d*)/ && do {
        $main_release  = $1;
        $point_release = $2;
        $minor_release = $3;
        $iteration     = $4;
    };
    $enVisionRevNumber = ($main_release * 1000000) + ($point_release * 10000) + ($minor_release * 100) + ($iteration * 1);
    # ex: R15.2.1.4  15020104
    #                MR
    #                  PR
    #                    mR
    #                      it
    return($enVisionRevNumber);
}

# -------------------------------------------------------------------------
# Common command line parsing...
sub ParseForCommonCommandLineArguments {
    local (*command_line) = @_;

    # Platform : 
    $command_line =~ s/:?-pl?a?t?f?o?r?m?\s*:\s*(\w+)//i && do {    # default XSeries, options XSeries|Diamond|Diamondx
        $cmd_opt{'TargetPlatform'} = "\U$1";
        $cmd_opt{'TargetPlatform'} !~ /XSERIES|DIAMOND|PHOENIX|DIAMONDX|DXV|ASLX/i && die "\tIncorrect -p[latform] invocation option!\n";
        $cmd_opt{'TargetPlatform'} eq "XSERIES"  && ($cmd_opt{'TargetPlatform'} = "XSeries");
        $cmd_opt{'TargetPlatform'} eq "DIAMOND"  && ($cmd_opt{'TargetPlatform'} = "Diamond");
        $cmd_opt{'TargetPlatform'} eq "PHOENIX"  && ($cmd_opt{'TargetPlatform'} = "Diamondx");
        $cmd_opt{'TargetPlatform'} eq "DIAMONDX" && ($cmd_opt{'TargetPlatform'} = "Diamondx");
        $cmd_opt{'TargetPlatform'} eq "DXV"      && ($cmd_opt{'TargetPlatform'} = "DxV");
        $cmd_opt{'TargetPlatform'} eq "ASLX"     && ($cmd_opt{'TargetPlatform'} = "ASLx");
        if ($cmd_opt{'TargetPlatform'} eq "Diamond") {          # 140114: OK for now, both Diamond and Diamondx only support D96; but soon, Diamondx will have more options.
#160504            $cmd_opt{'DigitalPinType'} = "D96";
        }
        if ($cmd_opt{'TargetPlatform'} eq "Diamondx") {
            $cmd_opt{'TargetOS'}       = "Unison";
        }
        if ($cmd_opt{'TargetPlatform'} eq "DxV") {
            $cmd_opt{'TargetOS'}       = "Unison";
            $cmd_opt{'Model'}          = "UDIG";
        }
        if ($cmd_opt{'TargetPlatform'} eq "ASLx") {
            $cmd_opt{'TargetOS'}       = "visualATE";
        }
    };

    # TargetOS : 
    $command_line =~ s/:?-ta?r?g?e?t?O?S?\s*:\s*(\w+)//i && do {    # default enVision, options enVision|ITE|Unison
        $cmd_opt{'TargetOS'} = "\U$1";
        $cmd_opt{'TargetOS'} !~ /ENVISION|ITE|UNISON|VISUALATE/i && die "\tIncorrect -t[esterOS] invocation option!\n";
        $cmd_opt{'TargetOS'} eq "ENVISION"  && ($cmd_opt{'TargetOS'} = "enVision");
        $cmd_opt{'TargetOS'} eq "UNISON"    && ($cmd_opt{'TargetOS'} = "Unison");
        $cmd_opt{'TargetOS'} eq "VISUALATE" && ($cmd_opt{'TargetOS'} = "visualATE");
        # if TargetOS is ITE, then force TargetPlatform = Diamond, Mode = STIL
        if ($cmd_opt{'TargetOS'} eq "ITE") {
            $cmd_opt{'TargetPlatform'} = "Diamond";
            $cmd_opt{'DigitalPinType'} = "D96";
            $cmd_opt{'Model'}          = "STIL";
        }
    };

    # DigitalPinType : 
    # need a DigitalInstrument flag : FX1/2/HV, DPIN96-16/32/64, (Stinger)    default D96, options D96|FX|GX|MP|D96GX
    $command_line =~ s/:?-digt?y?p?e?\s*:\s*(\w+)//i && do {    # default D96, options D96|FX|GX(Stinger)|MP(Tornado)
        $cmd_opt{'DigitalPinType'} = "\U$1";
        $cmd_opt{'DigitalPinType'} !~ /\bD96\b|FX|\bGX\b|MP|D96GX|DDP/i && die "\tIncorrect -Dig[Type] invocation option!\n";
    };

    # Model :
    $command_line =~ s/:?-mo?d?e?l?\s*:\s*(\w+)//i && do {      # default VLSI, options VLSI|CX|MSD|MSDI|STIL|UDIG
        $cmd_opt{'Model'} = "\U$1";
        $cmd_opt{'Model'} !~ /VLSI|CX|\bMSD\b|MSDI|STIL|UDIG/i && die "\tIncorrect -m[odel] invocation option!\n";
        # if Model is STIL, then force TargetPlatform = Diamond, DigitalPinType = D96, TargetOS = ITE
        if ($cmd_opt{'Model'} eq "STIL") {
            $cmd_opt{'TargetPlatform'} = "Diamond";
            $cmd_opt{'DigitalPinType'} = "D96";
            $cmd_opt{'TargetOS'}       = "ITE";
        }
    };

    # add ??
    # -r[emovePins] <RemovePinsListFileName>
    # -A[dd] <AddPinsListFileName>
    # -tr[igger] <TriggerPinName>
    # -l[og]
    # -his[tory]
    # -c <ConversionSetupFileName>
    # -C[ustomer] <CustomerKey>]
    # &write_ConversionSetupFile(@CommandLineOptions);

    # add in conclusions here?
    # ergo...
    if (($cmd_opt{'TargetPlatform'} eq "Diamond") && ($cmd_opt{'DigitalPinType'} !~ /D96/)) {          # 140114: OK for now, both Diamond and Diamondx only support D96; but soon, Diamondx will have more options.
        &UserMessage('Warning', "User-selected DigType ($cmd_opt{'DigitalPinType'}) is not valid for TesterPlatform ($cmd_opt{'TargetPlatform'}). Changing DigType to \'D96\'.");
        $cmd_opt{'DigitalPinType'} = "D96";
    }
    if (($cmd_opt{'TargetPlatform'} eq "Diamondx") && ($cmd_opt{'Model'} eq "VLSI")) {
        $cmd_opt{'DigitalPinType'} = "D96";
    }
    
}

# -------------------------------------------------------------------------
sub ParseObjects {
    local($CurrentPath, $CurrentFile, $enVisionData) = @_;
    #150708 $CurrentPath =~ s/\/$//;                                    # remove trailing '/'
    $ObjectPath = $CurrentPath;                                 # ???
    $File       = $CurrentFile;
#    $ExternalRefStackIndex++;
#    $ExternalRefStack[$ExternalRefStackIndex]->{'File'} = $File;
#    $ExternalRefStack[$ExternalRefStackIndex]->{'Path'} = $CurrentPath;
    #push(@ExternalRefStack, $ExternalRefElements);
    $FileType = (-e $cmd_opt{'AppendToProgram'}) ? $cmd_opt{'TargetOS'} : $cmd_opt{'Source'};
    
    #$enVisionData =~ s/\n\}\s*\n/\|/g;                          # change \n to '|' for matches
    $enVisionData =~ s/\/\/.*\n//g;                             # remove any // comments
    $enVisionData =~ s/\/\*.*?\*\///sg;                         # remove any /* ... */ comments
    $enVisionData =~ s/\n\}\s*\n/__EOO__/g;                     # change \n}\n to '__EOO__' for matches

    $enVisionData =~ s/^enVision\:\s*\"([^\"]+)\"\s*;//     && ($EvaHeader = $1);
    $enVisionData =~ s/^Unison\:U[\d\.]+\:S[\d\.]+\s*;//    && ($EvaHeader = $1);     # Unison header  Unison:U3.0:S5.3;
    $enVisionData =~ s/^Unison\:SyntaxRevision[\d\.]+\s*;// && ($EvaHeader = $1);     # Unison header  Unison:SyntaxRevision6.310000;
    
    #while ($enVisionData =~ s/^(\w+)\s+(\w*\s*\w*)\s*\{\s*([^|]*)\|//) {
    while ($enVisionData =~ s/^\s*(\w+)\s+(\w*\s*\w*)\s*\{\s*(.*?)__EOO__//s) {
        $ObjectType = $1;
        $ObjectName = $2;
        $ObjectData = $3;
        # __WaveformTable PatternGroup_Scan PatternGroup_Scan ==> PatternGroup_Scan__PatternGroup_Scan
        #150915 $ObjectName =~ s/(\w+)\s+(\w+)/$1__$2/;
        $ObjectName =~ s/(\w+)\s+(\w+)/$1\|\|$2/;
        $ObjectName =~ s/\s*$//;                                # remove trailing white space
        
        if (($ObjectType eq "ExternalRef") || ($ObjectType eq "__ExternalRef")) {
            $ParentFile = $File;
            $ParentPath = $ObjectPath;

            $ObjectName = "ExternalRef" . $ExternalRefCount++;
            ($debug == 9) && printf "%-35s %-22s %s/%s\n", $ObjectName, $ObjectType, $ObjectPath, $File;
            if ($ObjectData !~ /\w/) {
                printf"No File\n";
            }

            $ExternalRefStackIndex++;
            #$ExternalRefStack[$ExternalRefStackIndex]->{'File'} = $File;
            #$ExternalRefStack[$ExternalRefStackIndex]->{'Path'} = $CurrentPath;
            $Path = "./";                                       # defaulted Path
            $ObjectData =~ /Path\s*=\s*\"(.*?)\";/ && ($rawPath = $Path = $1);
            #150708 $Path =~ s/\.?\/$//;                                # remove trailing './' or '/'
            # $Path =~ s/^\.\///;                                 # remove './'
            $ObjectData =~ /File\s*=\s*\"(.*?)\";/ && ($File = $1);

            if ($File =~ s/([\/\.\~\$\w]*)\/([\w\.]+)$/$2/) { $Path = "$Path$1"; }
            
            $ExternalRefStack[$ExternalRefStackIndex]->{'Path'} = $Path;
            $ExternalRefStack[$ExternalRefStackIndex]->{'File'} = $File;

            #150708 if ($CurrentPath ne ".") { $NewPath = "$CurrentPath/$Path"; }
            #150708 else                     { $NewPath = "$Path"; }
            $NewPath = "$CurrentPath/$Path";
            #150708 $NewPath =~ s/\/\.\//\//g;                          # replace '/./' with '/'
            #150708 $NewPath =~ s/\.?\/$//;                             # remove trailing './' or '/'
            
            $FullFileName = "$NewPath/$File";
            $ObjectPath   = $NewPath;
            #($debug == 9) && printf "%-22s %-30s\n", $ObjectType, $FullFileName;
            #($debug == 9) && printf "%-35s %-22s %s/%s\n", $ObjectName, $ObjectType, $ObjectPath, $File;
            push(@ExternalRefdFiles, $FullFileName);

            $NavIndex++;
            $ObjectNavigator[$NavIndex]->{'ObjectName'} = $ObjectName;
            $ObjectNavigator[$NavIndex]->{'Type'}       = $ObjectType;
            $ObjectNavigator[$NavIndex]->{'Data'}       = $ObjectData;
            #150708 $ObjectNavigator[$NavIndex]->{'Path'}       = $ParentPath;
            $ObjectNavigator[$NavIndex]->{'Path'}       = $CurrentPath;
            $ObjectNavigator[$NavIndex]->{'File'}       = $ParentFile;
            $ObjectNavigator[$NavIndex]->{'RelPath'}    = $rawPath;
            $ObjectNavigator[$NavIndex]->{'AbsPath'}    = "$ParentPath/$ParentFile";
            $ObjectNavigator[0] = $NavIndex;
            
            #$NewPath = ;
            $NewFile = $File;

            if (-e $FullFileName) {
                #$nthEVO++;
                #open($FILEIDArray[$nthEVO], $FullFileName) || die "Couldn't open the $cmd_opt{'TargetOS'} file \"$FullFileName\".\n";
                open(EVO, $FullFileName) || die "Couldn't open the $FileType file \"$FullFileName\".\n";
                $/ = "__!!__";
                #170718 no longer supported.  $* = 1;                                         # enable multi-line matching          removing causes problems, use /m modifier??
                $EVOData = <EVO>;
            
                &ParseObjects($NewPath, $NewFile, $EVOData);    # recursive call to ParseObjects() ...
                close(EVO);
                #$nthEVO--;
            }
            else {
                &UserMessage('Error', "Couldn't find the $FileType file \"$FullFileName\".");
            }
            
            # $File = $ParentFile;
        }
        else {
            #($debug == 9) && printf "%-22s %-30s\n", $ObjectType, $ObjectName;
            $ObjectPath = $ExternalRefStack[$ExternalRefStackIndex]->{'Path'};
            #150708 $ObjectPath =~ s/\/$//;
            ($debug == 9) && printf "%-35s %-22s %s/%s\n", $ObjectName, $ObjectType, $ObjectPath, $File;
            push(@ObjectList, join(':', $ObjectType, $ObjectName));   # Fixed here: Object gets pushed a 2nd time after leaving a recursive ParseObjects()
            # $Objects{$ObjectType, $ObjectName}++;                   # there should never be a count > 1
            $ObjectData{$ObjectName}->{'Type'} = $ObjectType;
            $ObjectData{$ObjectName}->{'Data'} = $ObjectData;
            #150708 $ObjectData{$ObjectName}->{'Path'} = $ObjectPath;
            #150708 $ObjectData{$ObjectName}->{'File'} = $File;
            
            # ObjectData vs ObjectNavigator?              add in "->{'InsertionOrder'}" to ObjectData
            
            $NavIndex++;
            $ObjectNavigator[$NavIndex]->{'ObjectName'} = $ObjectName;
            $ObjectNavigator[$NavIndex]->{'Type'}       = $ObjectType;
            #150708 $ObjectNavigator[$NavIndex]->{'Data'}       = "";
            #150708 $ObjectNavigator[$NavIndex]->{'Path'}       = $ObjectPath;
            #150708 $ObjectNavigator[$NavIndex]->{'Path'}       = $ParentPath;
            $ObjectNavigator[$NavIndex]->{'Path'}       = $CurrentPath;          # clean up path ("DECT0_DM10_A2/.//.")
            $ObjectNavigator[$NavIndex]->{'File'}       = $File;
            #150708 $ObjectNavigator[$NavIndex]->{'File'}       = $ParentFile;
            $ObjectNavigator[0] = $NavIndex;
        }

#        push(@ObjectList, join(':', $ObjectType, $ObjectName));   # Object gets pushed a 2nd time after leaving a recursive ParseObjects()
        # $Objects{$ObjectType, $ObjectName}++;                   # there should never be a count > 1
#        $ObjectData{$ObjectName}->{'Type'} = $ObjectType;
#        $ObjectData{$ObjectName}->{'Data'} = $ObjectData;
#        $ObjectData{$ObjectName}->{'Path'} = $ObjectPath;
#        $ObjectData{$ObjectName}->{'File'} = $File;
    }
    #pop(@ExternalRefStack);
    #$ExternalRefElements = $ExternalRefStack[$#ExternalRefStack];
    #$File = $ExternalRefElements->{'File'};
    $ExternalRefStackIndex--;
    $File        = $ExternalRefStack[$ExternalRefStackIndex]->{'File'};
    $CurrentPath = $ExternalRefStack[$ExternalRefStackIndex]->{'Path'};
    $break = 1;
}

# -------------------------------------------------------------------------
sub create_PinNameColumns {
    local (*PinList, $offset) = @_;                             # ($offset, @PinList) = @_; swap order??
    local ($PinName, $MaxPinNameLength, $PinNameColumns, $MaxColumns, $x, $y, %tempPinNameArray);
    $MaxPinNameLength = 0;
    $PinNameColumns   = "";
    
    # Determine maximum PinName length
    foreach $PinName (@PinList) {
        if ($RemovePinsList{$PinName} >= 1) { next; }
        $PinName =~ s/^\%//;                                    # remove any leading column separator (%)
        if (length($PinName) > $MaxPinNameLength) { $MaxPinNameLength = length($PinName); }
    }

    # Iterate through @PinList, fill up 2-dimensional array %tempPinNameArray
    $x = 0;
    foreach $PinName (@PinList) {
        $PinName =~ s/^\%// && ($x++);                          # remove any leading column separator (%) and add blank column
        if ($RemovePinsList{$PinName}) { next; }                # if an unused pin, then next
        for $y (0..(length($PinName)-1)) { $tempPinNameArray{$x, $y} = substr($PinName, $y, 1); }
        $MaxColumns = $x;
        $x++;
    }
    
    # From %tempPinNameArray, create $PinNameColumns string
    for $y (0..($MaxPinNameLength-1)) {
        #100430 if ($offset > 0) { $PinNameColumns .= sprintf("%*s", $offset, " "); }
        #100916 if ($offset > 0) { $PinNameColumns .= sprintf("\t%*s", $offset, " "); }
        if ($offset > 0) { $PinNameColumns .= sprintf("%*s", $offset, " "); }
        for $x (0..$MaxColumns) { $PinNameColumns .= ($tempPinNameArray{$x, $y} =~ /\w/) ? $tempPinNameArray{$x, $y} : " "; }
        $PinNameColumns .= "\n";
    }
    
    # add "-------------------------" ???
    
    return($PinNameColumns);
}

# -------------------------------------------------------------------------
sub createSTIL_Date {
    # Www Mmm dd hh:mm:ss yyyy
    # Mon Sep 28 10:23:45 2009   need TimeZone %Z ??
    $STIL_Date = `date "+%a %b %d %H:%M:%S %Z %Y"`;
    chop($STIL_Date);
    return($STIL_Date);
}

# -------------------------------------------------------------------------
sub DetermineOperatingSystem {
#    $OperatingSystem = system"/bin/uname -s";
#if ( `/bin/uname -s` == "Linux" ) then
#   source ~build/.cshrc
#else if ( `/bin/uname -s` == "SunOS" ) then
#   source ~/.cshrc.sun
#else
#   echo "Don't have a .cshrc file for this OS"
#endif
    if    (-f "/etc/vfstab") { $cmd_opt{'OperatingSystem'} = "Solaris"; }
    elsif (-f "/etc/issue")  { $cmd_opt{'OperatingSystem'} = "Linux";   }
    else                     { $cmd_opt{'OperatingSystem'} = "???";     }
}

# -------------------------------------------------------------------------
sub DetermineLinuxOSVersion {
    # 
    $SystemCommand = "/usr/bin/lsb_release -d";
    $CentOS_Version  = `$SystemCommand`;
    if    ($CentOS_Version =~ /release\s+4\.6/) { return "CentOS4.6"; }
    elsif ($CentOS_Version =~ /release\s+6\.2/) { return "CentOS6.2"; }
    elsif ($CentOS_Version =~ /release\s+7\.2/) { return "CentOS7.2"; }
    else {
        &UserMessage('Error', "Invalid CentOS version. (Required: CentOS 4.6, CentOS 6.2, CentOS 7.2");
        return "";
    }
}

# -------------------------------------------------------------------------
sub UserMessage {
    local($ErrorType, $Message) = @_;
    printf "*** %-8s : %s\n", $ErrorType, $Message;
    # print ">>> Error    >>> Couldn't open the J750 pattern file \"$j750_file\".\n";
    # %ErrorType = ('Error', 1, 'Warning', 2, 'UserInfo', 3);
    if ($ErrorType eq "Error")    { $Errors->{'ErrorCount'}++; }
    if ($ErrorType eq "Warning")  { $Errors->{'WarningCount'}++; }
    if ($ErrorType eq "UserInfo") { $Errors->{'UserInfoCount'}++; }
}

# -------------------------------------------------------------------------
sub UNIXfy_directory {
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    local(*directory) = @_;
    #121017 ($debug) && printf "PC Path   : %s\n", $directory;
    
    $directory =~ s/\\/\//g;                                    # replace all PC '\' directory separators with Unix '/'

    # Replace drive (E:) with /node name             /bin/hostname ==> viper      uname -n
    $directory =~ /^([a-z])\:/i && do {
#        $this_node = `uname -n`;
#        $this_node =~ s/\n$//;
#        $directory =~ s/^([a-z])\:/\/$this_node/i;
#        &UserMessage('Error', "Drive $1 specified, replaced with \"\/$this_node\".");
    };
    
    @temp_leafs = split(/\//, $directory);

    $UNIXdirectory = "./";
    foreach $leaf (@temp_leafs) {
        $temp_leaf = "\L$leaf";                                 # lower case for matching
        opendir(DIR, $UNIXdirectory);
        @allfiles = readdir(DIR);                               # grep(!/^\./, readdir(DIR));
        closedir(DIR);
        $leaf_found = 0;
        foreach $subdir (@allfiles) {
            $temp_subdir = "\L$subdir";                         # lower case for matching
            if ($temp_subdir eq $temp_leaf) { $UNIXdirectory .= "$subdir/"; $leaf_found++; last; }
        }
        if (!$leaf_found) { $UNIXdirectory .= "$leaf/"; }       # if leaf not found, append last leaf (filename)
        $break = 1;
    }
    $UNIXdirectory =~ s/^\.\///;                                # remove leading './' and trailing '/'
    $UNIXdirectory =~ s/\/$//;
    
    #121017 ($debug) && printf "UNIX Path : %s\n", $UNIXdirectory;
    $directory = $UNIXdirectory;
}

# -------------------------------------------------------------------------
sub gcd {
}

# -------------------------------------------------------------------------
sub gcf {               # gcf == gcd ??
    #170330 use integer;
    my $gcf = shift || 1;
    while (@_) {
        my $next = shift;
        while($next) {
            #170330 my $r = $gcf % $next;
            my $r = remainder($gcf, $next);
            $r += $next if $r < 0;
            $gcf = $next;
            $next = $r;
        }
    }
    #170330 no integer;
    return($gcf);
}

# -------------------------------------------------------------------------
sub lcm {
    #170330 use integer;
    my $lcm = shift;
    foreach (@_) { $lcm *= $_ / gcf($_, $lcm) }
    #170330 no integer;
    return($lcm);
}

# -------------------------------------------------------------------------
# sub gcf {
#     my ($x, $y) = @_;
#     ($x, $y) = ($y, $x % $y) while $y;
#     return $x;
# }

# -------------------------------------------------------------------------
# sub lcm {
#     return($_[0] * $_[1] / gcf($_[0], $_[1]));
# }

# -------------------------------------------------------------------------
# Perl's modulo operator (a % b) is an integer operation. It will use the integer
# portion of the fractions a or b. Hence this function:
sub remainder {
    my ($a, $b) = @_;
    # return 0 unless $b && $a;
    # return $a / $b - int($a / $b);
    my $div = $a / $b;
    return($a - int($div) * $b);
}

# -------------------------------------------------------------------------
sub dec2hex {
    my $dec = int(shift);
    my $pref;
    if(shift) { $pref = '0x' } else { $pref = '' }
    my $hex = $pref . sprintf("%x", $dec);
    return($hex);
}

# -------------------------------------------------------------------------
sub hex2dec {          # add other functions from Perl_Math.txt on laptop, add description and usage.
    my $h = shift;
    $h =~ s/^0x//g;
    return(hex($h));
}

# -------------------------------------------------------------------------
sub dec2oct {
    my $dec = int(shift);
    my $oct = sprintf("%o", $dec);
    return($oct);
}

# -------------------------------------------------------------------------
sub oct2dec {
    my $o = shift;
    return(oct($o));
}

# -------------------------------------------------------------------------
sub dec2bin {                                                   # dec2bin(decimalnumber, bits)
    my $dec  = int(shift);
    my $bits = shift;                                           # bits: 4..32 
    my $bin  = unpack("B32", pack("N", $dec));                  # "B32": A bit string, high-to-low order, "N": A long in "network" order (??)
    substr($bin, 0, (32 - $bits)) = '';
    return($bin);
}

# -------------------------------------------------------------------------
sub bin2dec {
    my $bin  = shift;
    my $bits = length($bin);
    $bin = (32 - $bits) x '0' . $bin;
    my $dec = unpack("N", pack("B32", substr("0" x 32 . $bin, -32)));
    return($dec);
}

# -------------------------------------------------------------------------
sub isOdd {
    local($IntegerToCheck) = @_;
    if ($IntegerToCheck % 2 == 1) { return 1; }
    else                          { return 0; }
}

# -------------------------------------------------------------------------
sub isSubset {
    my($littleSet, $bigSet) = @_;
    my %hash;
    undef @hash{@$littleSet};
    delete @hash{@$bigSet};
    return !%hash;
}

# -------------------------------------------------------------------------
sub deep_copy {
    my $this = shift;
    if (not ref $this) {
        $this;
    }
    elsif (ref $this eq "ARRAY") {
        [map deep_copy($_), @$this];
    }
    elsif (ref $this eq "HASH") {
        +{map { $_ => deep_copy($this->{$_}) } keys %$this};
    }
    else {
        die "in deep_copy: what type of variable is $_?";
    }
}

# -------------------------------------------------------------------------
sub parseConfigFile {
    # determine enVision/Unison/ITE : $cmd_opt{'TargetOS'}
    # determine Simulator, on Tester, or local config file.
    # /u/bkordes/synchro_sim/bkordes_U4_1_1_DMDx_sim/pwrup/unison_config
    # HOME=/u/bkordes        $ENV{'HOME'}
    # or invocation option -cf /u/bkordes/synchro_sim/bkordes_U4_1_1_DMDx_sim/pwrup/unison_config
    # LTX_TESTER = bkordes_Mediatek_U5_1_X_GX_DMDx_sim
    # read SystemConfig (??)
    #150324 %ChannelsPerInstrument = ('DD1096', 96,
    #                          'HDVI',   72,
    #                          'DPS16',  16,
    #                          'VIS16',  16,
    #                          );
    &InitializeChannelsPerInstrument;                           # in 'UtilityFunctions.pl'
    
    $FirstAvailable_DD1096_Channel = 9999;
    $FirstAvailable_GX1_Channel    = 9999;
    $FirstAvailable_PECFX_Channel  = 9999;
    $FirstAvailable_DPS16_Channel  = 9999;
    $ConfigFile = "unison_config";
    
    if (-e $ConfigFile) {
        printf "\n>> Parsing Configuration file \"$ConfigFile\"...\n";
    }
    else {
        # create a 'default' configuration
# $UnisonConfig = HASH(0x96a1e38)
#    'Instruments' => HASH(0x9b3e354)
#       'PHX_DD1096_64' => 2
#       'PHX_GX1' => 6
#       'PHX_HDVI' => 1
#       'PHX_SDU' => 0
#    'Slots' => ARRAY(0x9b3e318)
#       0  'PHX_SDU'
#       1  'PHX_HDVI'
#       2  'PHX_DD1096_64'
#       3  empty slot
#       4  empty slot
#       5  empty slot
#       6  'PHX_GX1'
        #                  UnisonOS   DigModel   DigInstr
        # Diamond      ->  U4         VLSI       D96
        #              ->  U5         UDIG       D96
        # Diamondx     ->  U4         VLSI       D96
        #              ->  U5         UDIG       D96, GX1
        # XSeries      ->  U4         MSDI       FX
        #              ->  U5(.2)     UDIG       FX
        
        #160412 if ($UnisonRevNumber >= 5000000) {
            # Diamond
            if ($cmd_opt{'TargetPlatform'} eq "Diamond") {
                $UnisonConfig->{'Platform'}  = "DMD";
                $UnisonConfig->{'Slots'}[0]  = "DD1096_64";
                $UnisonConfig->{'Slots'}[1]  = "DD1096_32";
                $UnisonConfig->{'Slots'}[2]  = "DD1096_32";
                $UnisonConfig->{'Slots'}[3]  = "VIS16";
                $UnisonConfig->{'Slots'}[4]  = "DPS16";
                $UnisonConfig->{'Slots'}[6]  = "MULTIWAVE";
                $UnisonConfig->{'Slots'}[7]  = "DD1096_16";  # DMD_DD1096_16
                $UnisonConfig->{'Slots'}[8]  = "HDVI";
                $UnisonConfig->{'Slots'}[9]  = "DIBU";
            }
            # Diamondx
            elsif ($cmd_opt{'TargetPlatform'} eq "Diamondx") {
                # 'typical' system config...
                $UnisonConfig->{'Platform'}  = "PHX";
                $UnisonConfig->{'Slots'}[0]  = "SDU";
                $UnisonConfig->{'Slots'}[2]  = "DD1096_64";
                $UnisonConfig->{'Slots'}[6]  = "DD1096_64";
                $UnisonConfig->{'Slots'}[8]  = "DD1096_64";
                $UnisonConfig->{'Slots'}[9]  = "DD1096_32";
                $UnisonConfig->{'Slots'}[10] = "HDVI";
                if ($UnisonRevNumber >= 5000000) {
                $UnisonConfig->{'Slots'}[6]  = "GX1";
                }
                #$UnisonConfig->{'Slots'}[3]  = "PHX_DD1096_64";
                #$UnisonConfig->{'Slots'}[8]  = "PHX_DD1096_32";
                #$UnisonConfig->{'Slots'}[9]  = "PHX_DD1096_64";
                #$UnisonConfig->{'Slots'}[10] = "PHX_DD1096_32";
                #$UnisonConfig->{'Slots'}[11] = "PHX_DD1096_64";
                #$UnisonConfig->{'Slots'}[15] = "PHX_DD1096_64";
            }
            # XSeries
            elsif ($cmd_opt{'TargetPlatform'} eq "XSeries") {
                $UnisonConfig->{'Platform'}  = "XSeries";
                $UnisonConfig->{'Slots'}[13] = "TH_PECFX";
                $UnisonConfig->{'Slots'}[14] = "TH_PECFX";
                $UnisonConfig->{'Slots'}[15] = "TH_PECFX";
                $UnisonConfig->{'Slots'}[16] = "TH_PECFX";
                $UnisonConfig->{'Slots'}[18] = "TH_PECFX";
                $UnisonConfig->{'Slots'}[19] = "TH_PECFX";
                $UnisonConfig->{'Slots'}[20] = "TH_PECFX";
                $UnisonConfig->{'Slots'}[21] = "TH_PECFX";
            }
        #160412 }
            
        # from the {'Slots'}, generate {'Instruments'}...
        for $SlotIndex (0..$#{$UnisonConfig->{'Slots'}}) {
            if ($UnisonConfig->{'Slots'}[$SlotIndex] ne "") {
                $UnisonConfig->{'Instruments'}->{$UnisonConfig->{'Slots'}[$SlotIndex]} .= ",$SlotIndex";
                $UnisonConfig->{'Instruments'}->{$UnisonConfig->{'Slots'}[$SlotIndex]} =~ s/^,//;     # remove leading ','
            }
        }
        
        return(0);
    }
    open(CONFIG, $ConfigFile);
    $/ = "\n";
    while (<CONFIG>) {
        chop($config_line = $_);
# [infrastructure]
# type = DMDx
# variation = DMDx
# type = XS
# variation = EX
        $config_line =~ /^\s*type\s*=\s*(\w+)/ && do {
            $infrastructureType = $1;
            $UnisonConfig->{'Type'} = $infrastructureType;
            if ($infrastructureType eq "XS") {
                $UnisonConfig->{'Platform'}  = "XSeries";
            }
        };
        $config_line =~ /^\s*variation\s*=\s*(\w+)/ && do {
            $infrastructureVariation = $1;
            $UnisonConfig->{'Variation'} = $infrastructureVariation;
        };

        # Diamond/Diamondx...
# S6  = PHX_DD1096_64        , 982-7419-10-?-?
# S7  = PHX_HSIO             , 979-1363-00-?-?    ; HSIO[57..64]  HSIORX57P..HSIORX64N
# S9  = PHX_DD1096_32        , 982-7419-00-?-?
# S10 = PHX_HDVI             , 982-7642-00-?-?
# S17 = PHX_DPS16            , 982-6136-00-?-?
# S18 = PHX_VIS16            , 982-6194-00-?-?
# S0    = PHX_SDU                 , 974-1300-00-AA-?,    n/a
# S3    = PHX_PMVIx               , 979-1534-00-?-?
# S14   = PHX_GX1                 , 979-1597-00-BA-?
# S14 = PHX_GX1_256          , 979-1597-10-?-?
        $config_line =~ /^\s*S(\d+)\s*=\s*(DMD|PHX)_(DIBU|SDU|DD1096_16|DD1096_32|DD1096_64|GX1|GX1_256|DPS16|VIS16|HDVI|MULTIWAVE|QFVI|PMVIx|HSIO|MP1|PD1x|PSM1|THCTL)\s*,\s*/ && do {
            $Slot       = $1;
            $Platform   = $2;
            $Instrument = $3;

            if ($Instrument =~ /DIBU|SDU/) {
                $UnisonConfig->{'Platform'} = $Platform;
            }
            
            if ($Instrument =~ /DD1096/) {
                $IU = "DD1096";
                $ChannelStart = ($UnisonRevNumber >= 5000000) ? 0 : $ChannelsPerInstrument{$IU}*$Slot;              # Zero-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
                if ($ChannelStart < $FirstAvailable_DD1096_Channel) { $FirstAvailable_DD1096_Channel = $ChannelStart; }
            }
            if ($Instrument =~ /GX1/) {
                $IU = "GX1";
                $ChannelStart = 0;                              # Zero-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
            }
            if ($Instrument =~ /MP1/) {
                $IU = "MP1";
                # 80 (all 7 ports, ports 0-6) at 800Mbps
                # 48 (ports 0-3)   at 1066Mbps
                # DP_x   where x is port number
                # ports 0-4    DP_0_D0..9  (10 pins) DP_0_CP/CN diff pair    5x(10+2)  60
                # ports 5-6    DP_5_D0..7  ( 8 pins) DP_5_CP/CN diff pair    2x(8+2)   20 = 80
                $ChannelStart = 0;                              # Zero-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
            }
            if ($Instrument =~ /DPS16/) {
                $IU = "DPS16";
                $ChannelStart = ($UnisonRevNumber >= 5000000) ? 1 : $ChannelsPerInstrument{$IU}*$Slot + 1;          # One-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
                if ($ChannelStart < $FirstAvailable_DPS16_Channel) { $FirstAvailable_DPS16_Channel = $ChannelStart; }
            }
            if ($Instrument =~ /MULTIWAVE/) {
                $IU = "MULTIWAVE";
            }
            if ($Instrument =~ /VIS16/) {
                $IU = "VIS16";
                $ChannelStart = ($UnisonRevNumber >= 5000000) ? 1 : $ChannelsPerInstrument{$IU}*$Slot + 1;          # One-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
            }
            if ($Instrument =~ /HDVI/) {
                $IU = "HDVI";
                $ChannelStart = ($UnisonRevNumber >= 5000000) ? 1 : $ChannelsPerInstrument{$IU}*$Slot + 1;          # One-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
            }
            if ($Instrument =~ /PMVIx/) {
                $IU = "PMVIx";
                $ChannelStart = ($UnisonRevNumber >= 5000000) ? 1 : $ChannelsPerInstrument{$IU}*$Slot + 1;          # One-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
            }
            if ($Instrument =~ /QFVI/) {
                $IU = "QFVI";
            }
            if ($Instrument =~ /HSIO/) {
                $IU = "HSIO";
            }
            if ($Instrument =~ /PD1x/) {
                $IU = "PD1";
                $ChannelStart = 1;                              # One-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
            }
            if ($Instrument =~ /PSM1/) {
                $IU = "PSM1";
            }
            if ($Instrument =~ /THCTL/) {
                $IU = "THCTL";
            }
            $debug &&
                printf "\tSlot %-2d : %-15s [%-4d..%-4d]\n", $Slot, $Instrument, $ChannelStart, $ChannelStop;
            # $ChannelStart, $ChannelStop are only needed for non-Slot/Channel AdapterBoards (pre-U5)
            # Unison U5 Slot.Channel hash...
            #160412 if ($UnisonRevNumber >= 5000000) {
#                $Instrument = sprintf("%s_%s", $Platform, $Instrument);         # hmmm, maybe not, a PHX_DD1096_64 is same as a DMD_DD1096_64
                $UnisonConfig->{'Slots'}[$Slot] = $Instrument;
                $UnisonConfig->{'Instruments'}->{$Instrument} .= ",$Slot";
                $UnisonConfig->{'Instruments'}->{$Instrument} =~ s/^,//;     # remove leading ','
            #160412 }
        };
        
        # XSeries...
#    S2 = OCTAL_VI        , 974-122-00-?-?   , ovi  ; 1..8
#    S9 = DSP_AWG         , 974-121-00-?-?   , dsp  ; 1..2
#   S11 = DSP_DIGITIZER   , 974-120-00-?-?   , dsp  ; 3..4
#   S13 = TH_PECFX2       , 974-1061-00-?-?  , ovi
#    S13 = TH_PECHS        , 974-1060-00-?-?    , ovi
#    S13 = TH_PECHV      , 974-1062-00-?-?  , ovi
#    S13 = TH_PECFX        , 974-1008-04-?-?    , ovi  ;  96..111
#     S14  = DYN_DIG_PIN     , 974-217-00-?-?   , ddp  ; 65..80
#     S3    = HCOVI       , 974-1014-00-?-? , hcovi  ; 9..16
#     S3    = HEX_VI       , 974-230-00-?-? , ovi  ; 529..544
#     S3    = HEX_VIB       , 974-1025-00-?-?   , ovi  ; 529..544
#     S8   = POWER_VI      , 974-273-00-?-? , ovi  ; 1..2
#     S12  = DIGHR   , 974-240-00-?-?   , dighr  ; 1..2
#     S9   = AWGHR   , 974-239-00-?-?   , awghr  ; 1..2
#     S12  = DIGHS   , 974-241-01-?-?   , dighs  ; 1..2
#     S12  = DIGHSB  , 974-1004-01-?-?  , dighsb  ; 1..2
#     S9   = AWGHS   , 974-250-00-?-?   , awghs ; 1..2
#     S9   = AWGHSB   , 974-1005-00-?-? , awghsb ; 1..2
#     S9   = SWGHSB   , 974-1157-00-?-? , awghsb ; 1..2
#     S6   = HVVI   , 974-259-00-?-?    , hvvi ; 1..8
#     S15  = DYN_DIG_HVDP   , 974-242-00-?-?    , ddp ; 1..16
#    S5    = QTMU           , 974-1045-00-?-?   , qtmu ; 97..100
#    S5    = QTMP           , 974-1111-00-?-?   , qtmu ; 97..100
#     S8   = QFVI            , 974-1073-00-?-?  , qfvi  ; 1..4
#    S3   = DCTM            , 974-1123-01-?-?   , dctm ; 1..4
#     S6   = DVM_CHCD      , 974-1302-00-?-?    , ovi  ; 1..2
#     S8   = VS1K          , 974-1309-00-?-?    , ovi  ; 1..8
#    S13  = HSIO           , 974-1253-00-?-?    , ovi   ;   1..8
        $config_line =~ /^\s*S(\d+)\s*=\s*(TH_PEC[FX2|FX|HV|HS]+|DYN_DIG_PIN|DYN_DIG_HVDP|OCTAL_VI|HCOVI|HEX_VI[B]*|POWER_VI|HVVI)\s*,\s*/ && do {
            $Slot       = $1;
            $Instrument = $2;
            
            if ($Instrument =~ /TH_PECFX/) {
                $IU = "FX1";
                $ChannelStart = ($UnisonRevNumber >= 5000000) ? 0 : $ChannelsPerInstrument{$IU}*$Slot;              # Zero-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
                if ($ChannelStart < $FirstAvailable_PECFX_Channel) { $FirstAvailable_PECFX_Channel = $ChannelStart; }
            }
            if ($Instrument =~ /TH_PECFX2/) {
                $IU = "FX2";
                $ChannelStart = ($UnisonRevNumber >= 5000000) ? 0 : $ChannelsPerInstrument{$IU}*$Slot;              # Zero-based channel numbering
                $ChannelStop  = $ChannelStart + $ChannelsPerInstrument{$IU} - 1;
                if ($ChannelStart < $FirstAvailable_PECFX_Channel) { $FirstAvailable_PECFX_Channel = $ChannelStart; }
            }



            $debug &&
                printf "\tSlot %-2d : %-15s [%-4d..%-4d]\n", $Slot, $Instrument, $ChannelStart, $ChannelStop;

            $UnisonConfig->{'Slots'}[$Slot] = $Instrument;
            $UnisonConfig->{'Instruments'}->{$Instrument} .= ",$Slot";
            $UnisonConfig->{'Instruments'}->{$Instrument} =~ s/^,//;    # remove leading ','
        };
    }  # end of 'while (<CONFIG>)'
    printf "\n";
    
    close(CONFIG);
}

# -------------------------------------------------------------------------
sub read_CompressionAlgorithms {
#ex:
# gzip : Compress   : /net/viper1/kordes/bin/gzip   : .gz
# gzip : UnCompress : /net/viper1/kordes/bin/gunzip : .gz
    
    $compress_opt{"gzip", "Compress", ".gz"}   = "/usr/bin/gzip";       # "/net/viper1/kordes/bin/gzip";
    $compress_opt{"gzip", "UnCompress", ".gz"} = "/usr/bin/gunzip";     # "/net/viper1/kordes/bin/gunzip";
    return;
    
    $/ = "\n";                                          # read CompressionAlgorithm file line-by-line
    open(COMPRESSION, "$module_path/CompressionAlgorithms") || die 
        "Couldn't open the \"$module_path/CompressionAlgorithms\" file.\n";
    while (<COMPRESSION>) {
        s/\n//;
	s/\s*:/:/g;
	s/:\s*/:/g;
	($Algorithm, $Mode, $Command, $Extension) = split(/\:/, $_);
	$compress_opt{$Algorithm, $Mode, $Extension} = $Command;
    }
    close(COMPRESSION);
}

# -------------------------------------------------------------------------
sub EstablishKeywords {
    # Set either enVision or Unison keywords into Keyword map
    %Keyword = (# general
                'Comment',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Comment"       : "Comment", # vs. if (enVision), elsif (Unison)...
                'Expression',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__Expression"    : "Expr",   
                'String',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__String"        : "String",
                'Type',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Type"          : "Type",
                'True',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__True"          : "True",
                'False',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__False"         : "False",
                'Inherit',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Inherit"       : "Inherit",
                'Direction',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__Direction"     : "Direction",
                'Mode',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Mode"          : "Mode",
                # OperatorVariable object
                'OperatorVariable', ($cmd_opt{'TargetOS'} eq "Unison") ? "__OperatorVariable" : "OperatorVariable",
                'Value',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Value"         : "Value",
                'UserMode',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__UserMode"      : "UserMode",
                # PinType object
                'PinType',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__PinType"       : "PinType",
                'Type',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Type"          : "Type",
                'Mux',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__Mux"           : "Mux",
                'CurrentLimit',  ($cmd_opt{'TargetOS'} eq "Unison") ? "PinCurrent"      : "IccMax",
                'VoltageLimit',  ($cmd_opt{'TargetOS'} eq "Unison") ? "PinVoltage"      : "PowerSupply",
                'LoadCapacitance',($cmd_opt{'TargetOS'} eq "Unison") ? "LoadCapacitance" : "LoadComp",
                # AdapterBoard object
                'AdapterBoard',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__AdapterBoard"  : "AdapterBoard",
                'Pin',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__Pin"           : "Pin",
                'Name',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Name"          : "Name",
                'Ppid',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Ppid"          : "Ppid",
                'XCoord',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__XCoord"        : "XCoord",
                'Shape',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Shape"         : "Shape",
                'Connection',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__Connection"    : "Connection",
                'TesterChannel', ($cmd_opt{'TargetOS'} eq "Unison") ? "__TesterChannel" : "TesterCh",
                'MaxSite',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__MaxSite"       : "MaxSite",
                # Axis object
                'Axis',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Axis"          : "Axis",
                'Title',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Title"         : "Title",
                'NumberOfSteps', ($cmd_opt{'TargetOS'} eq "Unison") ? "__NumberSteps"   : "NumSteps",
                'ParameterVariance',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__ParameterVariance"  : "ParameterVariance",
                'SpecVariance',  ($cmd_opt{'TargetOS'} eq "Unison") ? ""                : "",
                'ExpressionVariance', ($cmd_opt{'TargetOS'} eq "Unison") ? "__ExpressionVariance" : "ExprVariance",
                'Start',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Start"         : "Start",
                'Stop',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Stop"          : "Stop",
                'Increment',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__Increment"     : "",
                #'PinGroup',      ($cmd_opt{'TargetOS'} eq "Unison") ? ""                : "",
                'Parameter',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__Param"         : "Param",
                'SendTo',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__SendTo"        : "SendTo",
                # PinGroup object
                'PinGroup',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__PinGroup"      : "PinGroup",
                'Group',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Group"         : "Group",
                # Bin and BinMap objects
                'Bin',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__Bin"           : "Bin_",
                'Number',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Number"        : "Number",
                'Result',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Result"        : "Result",
                'MaxCount',      ($cmd_opt{'TargetOS'} eq "Unison") ? ""                : "",
                'CheckOverFlow', ($cmd_opt{'TargetOS'} eq "Unison") ? "__CheckOverFlow" : "CheckOverFlow",
                'Color',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Color"         : "Color",
                'BinMap',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__BinMap"        : "BinMap",
                # Spec and Mask objects
                'Spec',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Spec"          : "Spec",
                'Category',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__Category"      : "Category",
                'ParamGlobals',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__ParamGlobals"  : "ParamGlobals",
                'MinConstraint', ($cmd_opt{'TargetOS'} eq "Unison") ? ""                : "MinConstraint",
                'MaxConstraint', ($cmd_opt{'TargetOS'} eq "Unison") ? ""                : "MaxConstraint",
                'BlankLine',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__BlankLine"     : "evBlankLine",
                'Mask',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Mask"          : "Mask",
                'MaskDefault',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__MaskDefault"   : "MaskDefault",
                # Flow and SubFlow objects
                'Flow',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Flow"          : "Flow_",
                'LoopExpression',($cmd_opt{'TargetOS'} eq "Unison") ? "__LoopExpression": "LoopExpr",
                'LoopNotify',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__LoopNotify"    : "LoopNotify",
                'SubFlow',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__SubFlow"       : "SubFlow",
                'Node',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Node"          : "Node",
                'XCoord',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__XCoord"        : "XCoord",
                'Port',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Port"          : "Port",
                #'',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__InputPosition"       : "UIFInfo",
                #'',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__PortPosition"        : "UIFPort",
                'SpecPairs',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__SpecPairs"     : "SpecPairs",
                'TestId',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__TestID"        : "TestId",
                'Exec',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Exec"          : "Exec",
                #'',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__NameFormat"          : "",
                'StartNode',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__StartNode"     : "StartState",
                #'',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__PortConnections"     : "",
                'Background',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__Background"    : "Background",
                'Data',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Data"          : "Data",
                #'',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__PortNumber"          : "",
                #'',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__PortSelect"          : "",
                # Levels object
                'Levels',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Levels"        : "Levels",
                'Column',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Column"        : "Column",
                'LevelsColumnType', ($cmd_opt{'TargetOS'} eq "Unison") ? "__LevelsColumnType" : "LevelsColumnType",
                "DigitalType",   ($cmd_opt{'TargetOS'} eq "Unison") ? "__DigitalType"   : "evDigitalType",
                "VIType",        ($cmd_opt{'TargetOS'} eq "Unison") ? "__VIType"        : "evPowerType",
                'Title',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Title"         : "Title",
                'ExecSeq',       ($cmd_opt{'TargetOS'} eq "Unison") ? "ExecSeq"         : "ExecSeq",
                'ForceValue',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__ForceValue"    : "PowerSupply",
                'MaxCurrent',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__HighClamp"     : "",
                'Delay',         ($cmd_opt{'TargetOS'} eq "Unison") ? "Delay"           : "Delay",
                # Margin object
                'Margin',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Margin"        : "Margin",
                # PatternMap object
                'PatternMap',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__PatternMap"    : "PatternMap",
                'DefaultSourcePath',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__DefaultSourcePath"   : "DefaultSourcePath",
                'DefaultBinaryPath',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__DefaultBinaryPath"   : "DefaultBinaryPath",
                'DefaultPatternGroup', ($cmd_opt{'TargetOS'} eq "Unison") ? "__DefaultPatternGroup" : "DefaultPatternGroup",
                'Pattern',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Pattern"       : "Pattern",
                'File',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__File"          : "File",
                'Path',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Path"          : "Path",
                'CachePath',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__CachePath"     : "CachePath",
                'Group',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Group"         : "Group",
                'Remove',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Remove"        : "evRemove",
                # AliasMap object
                'AliasMap',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__AliasMap"      : "AliasMap",
                # PatternGroup object
                'PatternGroup',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__PatternGroup"  : "PatternGroup",
                # PatternSequence object
                'PatternSequence', ($cmd_opt{'TargetOS'} eq "Unison") ? "__PatternSequence": "PatternSequence",
                'Thread',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Thread"        : "Thread",
                'Zipper',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Zipper"        : "Zipper",
                'Row',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__Row"           : "Row",
                'AutoBasePeriod',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__AutoBasePeriod": "evAutoBasePeriod",
                'PinModes',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__PinModes"      : "evPinModes",
                # PatternSetup object
                'PatternSetup',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__PatternSetup"  : "PatternSetup",
                'FormatSet',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__FormatSet"     : "",                   # UDIG
                'PinConfig',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__PinConfig"     : "evPinConfig",
                'Namespace',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__Namespace"     : "",                   # UDIG
                #'Row',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__Row"           : "Row",
                'PinsPC',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Pins"          : "evPins",
                'DirectionPC',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__Direction"     : "evDirection",
                'TimingModePC',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__TimingMode"    : "evTimingMode",
                'MuxPC',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Mux"           : "evMux",
                'DifferentialPC',($cmd_opt{'TargetOS'} eq "Unison") ? "__Differential"  : "evDifferential",
                'DrivePC',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Drive"         : "evDrive",
                'ComparePC',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__Compare"       : "evCompare",
                'TerminationPC', ($cmd_opt{'TargetOS'} eq "Unison") ? "__Termination"   : "evTermination",
                'ClockPC',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Clock"         : "evClock",
                'AliasPC',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Alias"         : "evAlias",
                'DrvFormatPC',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__DrvFormat"     : "evDrvFormat",
                'CmpFormatPC',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__CmpFormat"     : "evCmpFormat",
                'SubRowPC',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__SubRow"        : "evSubRow",
                'PatternList',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__PatternList"   : "evPatternList",
                'PatternBurstList', ($cmd_opt{'TargetOS'} eq "Unison") ? "__PatternBurstList" : "",         # UDIG
                'PatternBurst',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__PatternBurst"  : "",               # UDIG
                'Action',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Action"        : "",               # UDIG
                'StartLabel',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__StartLabel"    : "",               # UDIG
                'EndLabel',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__EndLabel"      : "",               # UDIG
                'StopCount',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__StopCount"     : "",               # UDIG
                'IgnoreCount',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__IgnoreCount"   : "",               # UDIG
                '', ($cmd_opt{'TargetOS'} eq "Unison") ? ""       : "",
                '', ($cmd_opt{'TargetOS'} eq "Unison") ? ""       : "",
                '', ($cmd_opt{'TargetOS'} eq "Unison") ? ""       : "",
                'Clocking',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__Clocking"      : "evClocking",
                'AutoBasePeriod',($cmd_opt{'TargetOS'} eq "Unison") ? "__AutoBasePeriod": "evAutoBasePeriod",
                'DisplayPeriod', ($cmd_opt{'TargetOS'} eq "Unison") ? "__DisplayPeriod" : "evDisplayPeriod",
                'Row_Clocking',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__Row"           : "evRow",
                'PrimaryPeriod', ($cmd_opt{'TargetOS'} eq "Unison") ? "__PrimaryPeriod" : "evPrimaryPeriod",
                'SyncRow',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__SyncRow"       : "evSyncRow",
                # Thread object
                #'Thread',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Thread"        : "Thread",
                'ExecutionType', ($cmd_opt{'TargetOS'} eq "Unison") ? "__ExecutionType" : "ExecutionType",
                #'Row',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__Row"           : "Row",
                'ThreadAction',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__ThreadAction"  : "ThreadAction",
                #'Pattern',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Pattern"       : "Pattern",
                'PatternLabel',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__PatternLabel"  : "PatternLabel",
                # SignalHeader object
                'SignalHeader',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__SignalHeader"  : "SignalHeader",
                'SegmentName',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__SegmentName"   : "SegmentName",
                'Signals',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Signals"       : "Signals",
                'Bus',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__Bus"           : "Bus",
                'Radix',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Radix"         : "Radix",
                'Hex',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__Hex"           : "Hex",
                'Decimal',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Decimal"       : "Decimal",
                'Octal',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Octal"         : "Octal",
                'Binary',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Binary"        : "Binary",
                'ByName',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__ByName"        : "ByName",
                'Constant',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__Constant"      : "Constant",
                'Duplicate',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__Duplicate"     : "Duplicate",
                'Scan',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Scan"          : "Scan",
                'ScanLength',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__ScanLength"    : "ScanLength",
                'Fill',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Fill"          : "Fill",
                'PostFill',      (($cmd_opt{'TargetOS'} eq "Unison") && ($cmd_opt{'Model'} eq "VLSI")) ? "__PostFill" : "PostFill",
                'PreFill',       (($cmd_opt{'TargetOS'} eq "Unison") && ($cmd_opt{'Model'} eq "VLSI")) ? "__PreFill"  : "PreFill",
                # Test object
                'Test',          ($cmd_opt{'TargetOS'} eq "Unison") ? (($UnisonRevNumber >= 3010000) ? "__TestGroup" : "__Test") : "Test",
                'Mask',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Mask"          : "Mask",
                'Entry',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Entry"         : "Entry",
                'Exit',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Exit"          : "Exit",
                'PortExpression',($cmd_opt{'TargetOS'} eq "Unison") ? "__PortExpression": "PortExpr",
                'PortAction',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__PortAction"    : "PortAction",
                'Title',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Title"         : "Title",
                'TestEnable',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__EnableExpression" : "Test_enable",
                'TestPins',      ($cmd_opt{'TargetOS'} eq "Unison") ? "TestPins"        : "Test_pins",
                'PatternThread', ($cmd_opt{'TargetOS'} eq "Unison") ? "TestPatterns"    : "Pattern_index",
                'TMResult',      ($cmd_opt{'TargetOS'} eq "Unison") ? "TM_RESULT"       : "tm_rslt",
                'TMPass',        ($cmd_opt{'TargetOS'} eq "Unison") ? "TM_PASS"         : "PASS",
                'TMFail',        ($cmd_opt{'TargetOS'} eq "Unison") ? "TM_FAIL"         : "FAIL",
                # TimeSet object
                'TimeSet',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__TimeSet"       : "TimeSet",
                #'Inherit',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Inherit"       : "Inherit",
                'T0',            ($cmd_opt{'TargetOS'} eq "Unison") ? "__T0"            : "evT0",
                'C0',            ($cmd_opt{'TargetOS'} eq "Unison") ? "__C0"            : "evC0",
                'C1',            ($cmd_opt{'TargetOS'} eq "Unison") ? "__C1"            : "evC1",     # ??
                'C2',            ($cmd_opt{'TargetOS'} eq "Unison") ? "__C2"            : "evC2",     # ??
                'C3',            ($cmd_opt{'TargetOS'} eq "Unison") ? "__C3"            : "evC3",     # ??
                'Row_TimeSet',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__Row"           : "Row",      # !!! Help indicates "evRow"
                'Pins_TimeSet',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__Pins"          : "evPins",
                'Drive_TimeSet', ($cmd_opt{'TargetOS'} eq "Unison") ? "__Drive"         : "evDrive",
                'Edge',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Edge"          : "evEdge",
                'EdgeOn',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Edge On"       : "evEdge On",
                'EdgePrecede',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__Edge Precede"  : "evEdge Precede",
                'EdgeData',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__Edge Data"     : "evEdge Data",
                'EdgeReturn',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__Edge Return"   : "evEdge Return",
                'Compare_TimeSet', ($cmd_opt{'TargetOS'} eq "Unison") ? "__Compare"     : "evCompare",
                'EdgeOff',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Edge Off"      : "evEdge Off",
                'SubRow_TimeSet',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__SubRow"      : "evSubRow",
                # WaveformTable object
                'WaveformTable', ($cmd_opt{'TargetOS'} eq "Unison") ? "__WaveformTable" : "WaveformTable",
                'Period',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Period"        : "Period",
                'Cell',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Cell"          : "Cell",
                'Data',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Data"          : "Data",
                'Color',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Color"         : "Color",
                'Other',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Other"         : "Other",
                'Serial',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Serial"        : "Serial",
                'Algorithm',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__Algorithm"     : "Algorithm",
                'DSPSendIncr',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__SendDspDataIncr" : "SendDspDataIncr",
                'CInvert',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__CInvert"       : "CInvert",
                'Drive',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Drive"         : "Drive",
                'Compare',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Compare"       : "Compare",
                'Expect',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Expect"        : "Expect",
                'EntryState',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__EntryState"    : "EntryState",
                'Control',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__Control"       : "Control",
                'Waveform',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__Waveform"      : "Waveform",
                'DriveHigh',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__DriveHigh"     : "DriveHigh",
                #'DriveHighIfOne',       ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                #'DriveHighIfZero',      ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                #'DriveHighIfOn',        ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                #'DriveHighIfOnAndOne',  ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                #'DriveHighIfOnAndZero', ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                'DriveLow',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__DriveLow"      : "DriveLow",
                'DriveData',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__DriveData"     : "DriveData",
                'DriveDataNot',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__DriveDataNot"  : "DriveDataNot",
                'DriveOff',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__DriveOff"      : "DriveOff",
                'DriveOn',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__DriveOn"       : "DriveOn",
                'EdgeMarker',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__EdgeMarker"    : "EdgeMarker",
                'CompareData',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__CompareData"      : "CompareData",
                'CompareDataNot',      ($cmd_opt{'TargetOS'} eq "Unison") ? "__CompareDataNot"   : "CompareDataNot",
                #'CompareHighIfOne',    ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                #'CompareHighIfZero',   ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                #'CompareLowIfZero',    ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                #'CompareLowIfOne',     ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                'CompareFloat',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__CompareFloat"     : "CompareFloat",
                'CompareFloatNot',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__CompareFloatNot"  : "CompareFloatNot",
                'CompareOpenData',     ($cmd_opt{'TargetOS'} eq "Unison") ? "__CompareOpenData"  : "CompareOpenData",
                #'CompareOpenDataNot',  ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                'CompareOpenFloat',    ($cmd_opt{'TargetOS'} eq "Unison") ? "__CompareOpenFloat" : "CompareOpenFloat",
                'CompareOpenFloatNot', ($cmd_opt{'TargetOS'} eq "Unison") ? "__CompareOpenFloatNot" : "CompareOpenFloatNot",
                'CompareClose',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__CompareClose"     : "CompareClose",
                'CaptureData',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__CaptureData"      : "CaptureData",
                # UDIG
                'FormatSet',           ($cmd_opt{'TargetOS'} eq "Unison") ? "__FormatSet"        : "",
                'AliasMap',            ($cmd_opt{'TargetOS'} eq "Unison") ? "__AliasMap"         : "",
                #'',      ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                #'',      ($cmd_opt{'TargetOS'} eq "Unison") ? ""      : "",
                # WaveformCapture object
                'WaveformCapture',  ($cmd_opt{'TargetOS'} eq "Unison") ? "__WaveformCapture"  : "WaveformCapture",
                'ReferenceSegment', ($cmd_opt{'TargetOS'} eq "Unison") ? "__ReferenceSegment" : "evReferenceSegment",
                'Start',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Start"         : "evStart",
                'Stop',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Stop"          : "evStop",
                'Pins',          ($cmd_opt{'TargetOS'} eq "Unison") ? "__Pins"          : "evPins",
                'Enable',        ($cmd_opt{'TargetOS'} eq "Unison") ? "__Enable"        : "evEnable",
                'Merge',         ($cmd_opt{'TargetOS'} eq "Unison") ? "__Merge"         : "evMerge",
                'DriveEnable',   ($cmd_opt{'TargetOS'} eq "Unison") ? "__DriveEnable"       : "evDriveEnable",
                'ResponseEnable',($cmd_opt{'TargetOS'} eq "Unison") ? "__ResponseEnable"    : "evResponseEnable",
                'ResponseVoh',   ($cmd_opt{'TargetOS'} eq "Unison") ? ""   : "",
                'ResponseVol',   ($cmd_opt{'TargetOS'} eq "Unison") ? ""   : "",
                'ScopeHi',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__ScopeHi"       : "",
                'ScopeLo',       ($cmd_opt{'TargetOS'} eq "Unison") ? "__ScopeLo"       : "",
                #'',($cmd_opt{'TargetOS'} eq "Unison") ? ""   : "",

                'ExternalRef',  '__ExternalRef',          # ExternalRef object
                'TestProg',     '__TestProg',             # TestProg
                'TPHeader',     '__TPHeader',
                'ParamCheck',   '__ParamCheck',
                '', ($cmd_opt{'TargetOS'} eq "Unison") ? ""       : "",
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                '', '',
                );
    #// ExternalRef object
    #Keyword["ExternalRef"]    = (user_env.output_mode == UNISON) ? "__ExternalRef"    : "ExternalRef";
    #// TestProg object
    #Keyword["TestProg"]       = (user_env.output_mode == UNISON) ? "__TestProg"       : "TestProg";
    #Keyword["TPHeader"]       = (user_env.output_mode == UNISON) ? "__TPHeader"       : "TPHeader";
    #Keyword["Comment"]        = (user_env.output_mode == UNISON) ? "__Comment"        : "Comment";
    #Keyword["ParamCheck"]     = (user_env.output_mode == UNISON) ? "__ParamCheck"     : "ParamCheck";
    #Keyword["Flow"]           = (user_env.output_mode == UNISON) ? "__Flow"           : "Flow_";
    #Keyword["PatternMap"]     = (user_env.output_mode == UNISON) ? "__PatternMap"     : "PatternMap";
    #Keyword["BinMap"]         = (user_env.output_mode == UNISON) ? "__BinMap"         : "BinMap";

    #// Flow and SubFlow objects
    #Keyword["Flow"]           = (user_env.output_mode == UNISON) ? "__Flow"           : "Flow_";
    #Keyword["SubFlow"]        = (user_env.output_mode == UNISON) ? "__SubFlow"        : "SubFlow";
    #Keyword["LoopExpression"] = (user_env.output_mode == UNISON) ? "__LoopExpression" : "LoopExpr";
    #Keyword["LoopNotify"]     = (user_env.output_mode == UNISON) ? "__LoopNotify"     : "LoopNotify";
    #Keyword["Node"]           = (user_env.output_mode == UNISON) ? "__Node"           : "Node";
    #Keyword["XCoord"]         = (user_env.output_mode == UNISON) ? "__XCoord"         : "XCoord";
    #Keyword["InputPosition"]  = (user_env.output_mode == UNISON) ? "__InputPosition"  : "UIFInfo";
    #Keyword["Port"]           = (user_env.output_mode == UNISON) ? "__Port"           : "Port";
    #Keyword["PortPosition"]   = (user_env.output_mode == UNISON) ? "__PortPosition"   : "UIFPort";
    #Keyword["TestID"]         = (user_env.output_mode == UNISON) ? "__TestID"         : "TestId";
    #//#Keyword["Node"]           = (user_env.output_mode == UNISON) ? "__SpecPairs"        : "Node";
    #Keyword["Exec"]           = (user_env.output_mode == UNISON) ? "__Exec"           : "Exec";
    #//#Keyword["Node"]           = (user_env.output_mode == UNISON) ? "__PortSelect"       : "Node";
    #Keyword["PortNumber"]     = (user_env.output_mode == UNISON) ? "__PortNumber"     : "PortNumber";
    #Keyword["StartNode"]      = (user_env.output_mode == UNISON) ? "__StartNode"      : "StartState";

    #Keyword[""] = (user_env.output_mode == UNISON) ? "" : "";
    #Keyword[""] = (user_env.output_mode == UNISON) ? "" : "";
    #Keyword[""] = (user_env.output_mode == UNISON) ? "" : "";
    #Keyword[""] = (user_env.output_mode == UNISON) ? "" : "";

}

# -------------------------------------------------------------------------
sub AddToObjectList {                                           # &AddToObjectList("OperatorVariable", $flag_name);
    local($ObjectType, $ObjectName) = @_;

    # checking Pin, PinGroup, OperatorVariable, Parameter, Test, ETest, Pattern, Bin
    $DefinedObjects{$ObjectType, $ObjectName}++;
    ($DefinedObjects{$ObjectType, $ObjectName} > 1) && return;
    
    if (exists($ObjectTypeLUT{$ObjectName}) && ($DefinedObjects{$ObjectType, $ObjectName} == 1)) {
        $ObjectTypeLUT{$ObjectName} .= ",$ObjectType";
    }
    else {
        $ObjectTypeLUT{$ObjectName}  = "$ObjectType";
    }
}

# -------------------------------------------------------------------------
sub CheckForMultiplyDefinedObjects {
    foreach $ObjectName (sort keys (%ObjectTypeLUT)) {
        if ($ObjectTypeLUT{$ObjectName} =~ /,/) {
            $Message = sprintf("Object %-20s multiply-defined as : %s", "\"$ObjectName\"", $ObjectTypeLUT{$ObjectName});
            &UserMessage('Warning', "$Message");
        }
    }
    # Check ObjectNames against Reserved Word List...
}

# -------------------------------------------------------------------------
sub ExpandPinGroup {
    local($PinExpr, *pins) = @_;
    if (exists($PinGroup{$PinExpr})) {
        $temp_pins = $PinGroup{$PinExpr};
        $temp_pins =~ s/\+$//;
        my @tempPins = split(/\+/, $temp_pins);
        foreach $PinExpr (@tempPins) {
            &ExpandPinGroup($PinExpr, *pins);
        }
    }
    else {
        #
        if (!exists($RemovePinsList{$PinExpr})) {
            $pins .= "$PinExpr+";
        }
    }
}
    
# -------------------------------------------------------------------------
sub expandPinExpression {
    local($PinExpr) = @_;
    my $tempPins = "";
    @tempPins = split(/\s*\+\s*/, $PinExpr);
    foreach $tempPin (@tempPins) {
        if (exists($PinGroup{$tempPin})) {                      # use recursion, call expandPinExpression again?
            @tempPins2 = split(/\s*\+\s*/, $PinGroup{$tempPin});
            foreach $tempPin2 (@tempPins2) {
                if (exists($PinGroup{$tempPin2})) {
                    @tempPins3 = split(/\s*\+\s*/, $PinGroup{$tempPin2});
                    foreach $tempPin3 (@tempPins3) {
                        if (exists($PinGroup{$tempPin3})) {
                            @tempPins4 = split(/\s*\+\s*/, $PinGroup{$tempPin3});
                            foreach $tempPin4 (@tempPins4) {
                                if (exists($PinGroup{$tempPin4})) {
                                    @tempPins5 = split(/\s*\+\s*/, $PinGroup{$tempPin4});
                                    foreach $tempPin5 (@tempPins5) {
                                        if (!exists($RemovePinsList{$tempPin5})) {
                                            $tempPins .= "+$tempPin5";
                                        }
                                    }
                                }
                                else {
                                    if (!exists($RemovePinsList{$tempPin4})) {
                                        $tempPins .= "+$tempPin4";
                                    }
                                }
                            }
                        }
                        else {
                            if (!exists($RemovePinsList{$tempPin3})) {
                                $tempPins .= "+$tempPin3";
                            }
                        }
                    }
                }
                else {
                    if (!exists($RemovePinsList{$tempPin2})) {
                        $tempPins .= "+$tempPin2";
                    }
                }
                #$tempPins .= sprintf("+%s", &expandPinExpression($more_tempPin));
            }
        }
        else {
            if (!exists($RemovePinsList{$tempPin})) {
                $tempPins .= "+$tempPin";
            }
        }
    }
    $tempPins =~ s/^\+//;                                       # remove leading '+'
    return($tempPins);
}
    
# -------------------------------------------------------------------------
sub expandPinExpression2 {
    local($PinExpr) = @_;
#    $PinGroup{$pin_group}
#    $PinRecords{$pinName}
#   pingroup|pin +|- pingroup|pin
    local $tempPins = "";
    local $PinElement;
    local @tempPinArray;
    $PinExpr =~ s/\-/\+\-/g;                                    # replace all subtracted pins (-) with (+-) for splitting
    @tempPinArray = split(/\s*\+\s*/, $PinExpr);
    foreach $PinElement (@tempPinArray) {
        if ($PinElement =~ s/^\-//) { $SubtractingPin = 1; } else { $SubtractingPin = 0; }
        # is PinElement a PinGroup
        if ($PinGroup{$PinElement}) {
            $tempPins .= &expandPinExpression2($PinGroup{$PinElement});
        }
        # the pin element is a Pin
        elsif ($PinRecords{$PinElement}) {
            $tempPins .= sprintf("+%s$PinElement", $SubtractingPin ? "-" : "");
        }
        else {
            #print "Pin Element $PinElement is neither a Pin or a PinGroup\n";
        }
    }
    # remove any Subtracted pins...
    while ($tempPins =~ s/\+\-(\w+)//) { $subPin = $1; $tempPins =~ s/\+\b$subPin\b//; }
    $tempPins =~ s/^\+//;                                       # remove leading '+'
    return($tempPins);
}

# -------------------------------------------------------------------------
sub numerically { $a <=> $b; }
    
# -------------------------------------------------------------------------
sub alphanumerically { $a cmp $b; }
    
# -------------------------------------------------------------------------
sub reverse_order { $b cmp $a; }
    
# -------------------------------------------------------------------------
sub InitializeChannelsPerInstrument {
    %ChannelsPerInstrument = ('DIBU_CBITS', '64',
                              'SDU_CBITS',  '128',
                              'DPIN96',     '96',
                              'DD1096',     '96',
                              'DPIN96,GX1', '96',
                              'HDVI',       '72',
                              'VIS16',      '16',
                              'DPS16',      '16',
                              'DIGMW',      '4',                # Channels 1-4
                              'AWGMW',      '4',                # Channels 5-8
                              'PMVIx',      '72',
                              'HSIO',       '8',
                              # XSeries
                              'FX1',        '16',
                              'FX2',        '32',
                              # Diamondx
                              'GX1',        '192',
                              'MP1',        '80',
                              'PD1',        '320',
                              #'', '',
                              #'', '',
                              );
    %InstrumentLUT = ('D96',   'DPIN96',
                      'FX',    'FX1',        # FX1, FX2, FXHS, FXHV
                      'MP',    'MP1',
                      'GX',    'GX1',
                      'D96GX', 'DPIN96,GX1',
                      'VIS16', 'VIS16',
                      'HDVI',  'HDVI',
                      'Pixel', 'PD1',
                      #'', '',
                      );
}

# -------------------------------------------------------------------------
sub InitializeD2PMap {                                          # 
    %D2P_SlotMap = ('0',  '14',                                 # DPIN96
                    '1',  '15',                                 # DPIN96 (optional)
                    '2',  '12',                                 # DPIN96 (optional)
                    '3',  '13',                                 # DPIN96 (optional)
                    '4',  '10',                                 # DPS16
                    '5',  '11',                                 # VIS16
                    '6',  '8',                                  # HDVI
                    '7',  '9',                                  # MULTIWAVE
                    '8',  '6',                                  # DPIN96 (optional)
                    '9',  '0');                                 # SDU
}

# -------------------------------------------------------------------------
sub InitializeD96GXCompatibilityMap {                           # from Stinger_Interposer_netlist_012113 (Mike Davis, Chuck Cook)
    %D96GX_Map = ('0',  '70',
                  '1',  '71',
                  '2',  '72',
                  '3',  '73',
                  '4',  '74',
                  '5',  '75',
                  '6',  '78',
                  '7',  '79',
                  '8',  '80',
                  '9',  '81',
                  '10', '82',
                  '11', '83',
                  '12', '84',
                  '13', '85',
                  '14', '86',
                  '15', '87',
                  '16', '88',
                  '17', '89',
                  '18', '92',
                  '19', '93',
                  '20', '94',
                  '21', '95',
                  '22', '96',
                  '23', '97',
                  '24', '98',
                  '25', '99',
                  '26', '100',
                  '27', '101',
                  '28', '102',
                  '29', '103',
                  '30', '106',
                  '31', '107',
                  '32', '108',
                  '33', '109',
                  '34', '110',
                  '35', '111',
                  '36', '112',
                  '37', '113',
                  '38', '114',
                  '39', '115',
                  '40', '116',
                  '41', '117',
                  '42', '120',
                  '43', '121',
                  '44', '122',
                  '45', '123',
                  '46', '124',
                  '47', '125',
                  '48', '138',
                  '49', '139',
                  '50', '140',
                  '51', '141',
                  '52', '142',
                  '53', '143',
                  '54', '144',
                  '55', '145',
                  '56', '146',
                  '57', '147',
                  '58', '148',
                  '59', '149',
                  '60', '150',
                  '61', '151',
                  '62', '152',
                  '63', '153',
                  '64', '154',
                  '65', '155',
                  '66', '158',
                  '67', '159',
                  '68', '160',
                  '69', '161',
                  '70', '162',
                  '71', '163',
                  '72', '164',
                  '73', '165',
                  '74', '166',
                  '75', '167',
                  '76', '168',
                  '77', '169',
                  '78', '172',
                  '79', '173',
                  '80', '174',
                  '81', '175',
                  '82', '176',
                  '83', '177',
                  '84', '178',
                  '85', '179',
                  '86', '180',
                  '87', '181',
                  '88', '182',
                  '89', '183',
                  '90', '186',
                  '91', '187',
                  '92', '188',
                  '93', '189',
                  '94', '190',
                  '95', '191',
                 );
}

# -------------------------------------------------------------------------
sub DetermineMaxRPTCount {
    $MAX_DPM_RPT = 2047;
    $MAX_CPM_RPT = 65535;
        
    %MaxRPTCount = ('CPM',     $MAX_CPM_RPT,
                    'DPM',     $MAX_DPM_RPT,
                    'Generic', '2147483647',
                    );
}

# -------------------------------------------------------------------------
sub write_ConversionSetupFile {
    # Conversion Setup file
    # provide all invocation options, comment out the ones not used.
    local($ConversionSetupFileName, @CommandLineOptions) = @_;

    #$ConversionSetupFileName = sprintf("./%s",
    #                                   # Design|Mask|MyC5053
    #                                   "IGXLWorkbookConversionSetup");     # IGXLWorkbookConversionSetup -vs- WorkbookProcessorConversionSetup
    open(SETUP, ">$ConversionSetupFileName");
    for $Index (0..$#CommandLineOptions) {
        if ($CommandLineOptions[$Index] =~ /^(-[\w+])/) {
            printf SETUP "%-10s %s\n",
                         $CommandLineOptions[$Index],
                         ($CommandLineOptions[$Index] !~ /^-lo?g?[AN]?|^-CPG|^-no?p?a?t?t?e?r?n?|-fla?t?t?e?n?|-Us?e?U?C?S?T?/i) ? $CommandLineOptions[$Index+1] : "";
               
        }
    }
    close(SETUP);
    chmod(0777, $ConversionSetupFileName);                      # give script executable rights
}

# -------------------------------------------------------------------------
sub buildCompileScript {
    local($WhichConverter) = @_;
    $CompileScriptName = sprintf("./$TargetDir%s/%s%s",
                                 ($cmd_opt{'TargetOS'} eq "Unison") ? (($Customer eq "Microchip") ? "/$ScriptsDir" : "/$ProgramDir") : "",
                                 (($cmd_opt{'Model'} eq "CX") || ($cmd_opt{'Model'} eq "MSD")) ? "$PatSrcDir/" : "",
                                 (($cmd_opt{'Model'} eq "CX") || ($cmd_opt{'Model'} eq "MSD") || ($cmd_opt{'Model'} eq "MSDI")) ? "Compile$cmd_opt{'Model'}\Patterns" : "Compile$cmd_opt{'Model'}\Patterns");

    open(SCRIPT, ">$CompileScriptName");
    printf SCRIPT "#!/bin/csh -f\n";
    printf SCRIPT "#===================================================================\n";
    printf SCRIPT "#\n";
    
    printf SCRIPT "#  Compiles the %s %s pattern(s).\n",                # Fusion vs. enVision, DMSD ???, just create if {} elsif {} structure???
                   $cmd_opt{'TargetOS'},
                   ($cmd_opt{'Model'} eq "CX") ? "CX" : "$cmd_opt{'Model'}-model";
    
    printf SCRIPT "#\n";
    printf SCRIPT "#  %-6s   Created by %s Conversion, Rev. $rev\n", $date, $WhichConverter;
    printf SCRIPT "#\n";
    printf SCRIPT "#===================================================================\n";

    if (($cmd_opt{'Model'} eq "CX") || ($cmd_opt{'Model'} eq "MSD")) {
        #180328 for $nthPattern (0..$patternCount) {
        for $nthPattern (1..$PatternData[0]->{'PatternCount'}) {
            $SourceFile = "$PatternData[$nthPattern]->{'patternName'}" . ".ds";
            $ObjectFile = "$PatternData[$nthPattern]->{'patternName'}" . ".do";
            printf SCRIPT "/ltx/com/DDas %s%-35s -o %s\n",
                          ($cmd_opt{'Model'} eq "MSD") ? "-target fx1 " : "",    # default is: -target cx
                          "$SourceFile",                        # "$cmd_opt{'PatternSourcePath'}/$SourceFile" ???
                          "$ObjectFile";                        # "$cmd_opt{'PatternObjectPath'}/$ObjectFile" ???
        }
    }
    # DDas -w <evaFile> SourceFile -o ObjectFile
    elsif ($cmd_opt{'TargetOS'} eq "enVision") {
        printf SCRIPT "epc -t %s %s-c %s\n",                    # epc -t VX4 -svm -g xxx.eva creates "CompilePatterns", "gdm7201_chip_StdPatGrp_CompilePats", "gdm7201_chip_StdPatGrp_epc.epi"
                      $cmd_opt{'DigitalSubSystem'},             # DNT, VX500, VX4, FX1
#                      $ScanVecCount ? "-svm " : "",             # if scan, specify -svm   
                      "-svm ",                                  # force -svm
                      $eva_FileName;
    }
    elsif ($cmd_opt{'TargetOS'} eq "Unison") {
        printf SCRIPT "upc %s-c %s\n",                          # upc -d D96 -c <TestProg>.una
                      ($cmd_opt{'Model'} eq "UDIG") ? "" : $cmd_opt{'TargetPlatform'} =~ /Diamond|Phoenix/ ? "-d D96 " : "-d FX ",
                      #"-svm ",                                  # force -svm
                      $una_FileName;
    }
    elsif ($cmd_opt{'TargetOS'} eq "ITE") {
        # from the jobs sub-directory...
        # /usr/dmd/current/system/bin/dsc -FI1 -MF -TDPIN96 -V0 -S -Wall  ../patterns/pattern_scan_group_ALL.stil
        # Usage: dsc <filename.stil> -T<type> -V<version> [-F<format version>] [-O<output dir>]     [-I<infolevel>] [-W<warnings>] [-M<mode>] [-MF] [-D<include dir>...] [-S] [-FI<0/1>] [-FL<level>] [-FR]       [-TL] [-DT] [-FS] [-SC<8/16/32>] [-DBG] [-CC<cycle type>] [-P]
    }
    
    close(SCRIPT);
    chmod(0777, $CompileScriptName);                            # give script executable rights
}

# -------------------------------------------------------------------------
sub buildApplicationLibraryCompileScript {
    local($WhichConverter) = @_;

    # build script to compile the Application Library...
    $MethodCompileScriptName = sprintf("./$TargetDir%s/%s",
                                       ($Customer eq "Microchip") ? "/$ScriptsDir" : "/$ProgramDir",
                                       "CompileApplicationLibrary");
    open(SCRIPT, ">$MethodCompileScriptName");
    printf SCRIPT "#!/bin/csh -f\n";
    printf SCRIPT "#===================================================================\n";
    printf SCRIPT "#\n";
    printf SCRIPT "#  %-6s   Created by %s Conversion, Rev. $rev\n", $date, $WhichConverter;
    printf SCRIPT "#\n";
    printf SCRIPT "#===================================================================\n";
    # MethodCompiler -force -g -f <>.una
    printf SCRIPT "MethodCompiler -f $una_FileName\n";

    close(SCRIPT);
    chmod(0777, $MethodCompileScriptName);                      # give script executable rights
}
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

$result = 1;            # Return flag for require()


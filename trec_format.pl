use strict;

my $infile = shift @ARGV;
my $firstname = shift @ARGV;
my $lastname = shift @ARGV;

open(INFILE, "<$infile");

my $id = 0;

while(<INFILE>)
{
    chomp;
    my $currfile = $_;
    $id++;
    my $outstr = "";
    
    open(CURRFILE, "<$currfile");

    $outstr = "<DOC>\n<DOCNO>$firstname" . "_" . "$lastname" . "_" . "$id</DOCNO>\n";

    while(<CURRFILE>)
    {
	chomp;
	$outstr .= $_ . "\n";
    }

    $outstr .= "</DOC>\n";

    close(CURRFILE);

    open(OUTFILE, ">$currfile");

    print OUTFILE $outstr;

    close(OUTFILE);

}

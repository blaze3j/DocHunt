BEGIN { 
  print "// ";
  print "// Warning: This file is automatically generated";
  print "// ";
  print "";
  print "#ifndef INDRI_WALKER_HPP";
  print "#define INDRI_WALKER_HPP";
  print "";
  print "namespace indri { ";
  print "  namespace lang { ";
  print "    class Walker { ";
  print "    public:";
  print "      virtual ~Walker();";
  print "      virtual void defaultBefore( class Node* n );";
  print "      virtual void defaultAfter( class Node* n );";
  print "";
}

"class" == $1 {
  printf "      virtual void before( class %s* n );\n", $2;
  printf "      virtual void after( class %s* n );\n", $2, $2;
}

END {
  print "   };";
  print " }";
  print "}";
  print "";
  print "#endif // INDRI_WALKER_HPP";
  print "";
}


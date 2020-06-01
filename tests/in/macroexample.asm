COPY    START    0
.
. This is a macro definition
.
RDBUFF  MACRO    &INDEV,&BUFADR,&RECLTH
        CLEAR    X
        CLEAR    A
        CLEAR    S
        +LDT     #4096
        TD       =X'&INDEV'
        JEQ      *-3
        RD       =X'&INDEV'
        COMPR    A,S
        JEQ      *+11
        STCH     &BUFADR,X
        TIXR     T
        JLT      *-19
        STX      &RECLTH
        MEND
WRBUFF  MACRO    &OUTDEV,&BUFADR,&RECLTH
        CLEAR    X
        LDT      &RECLTH
        LDCH     &BUFADR,X
        TD       =X'&OUTDEV'
        JEQ      *-3
        WD       =X'&OUTDEV'
        TIXR     T
        JLT      *-14
        MEND
FIRST   STL      RETADR
CLOOP   RDBUFF   F1,BUFFER,LENGTH
        LDA      LENGTH
        COMP     #0
        JEQ      ENDFIL
        WRBUFF   05,BUFFER,LENGTH
        J        CLOOP
ENDFIL  WRBUFF   05,EOF,THREE
        J        @RETADR
EOF     BYTE     C'EOF'
THREE   WORD     3
RETADR  RESW     1
LENGTH  RESW     1
BUFFER  RESB     4096
        END      FIRST
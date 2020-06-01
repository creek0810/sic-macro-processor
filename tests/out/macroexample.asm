COPY    START    0
FIRST   STL      RETADR
.CLOOP   RDBUFF   F1,BUFFER,LENGTH
CLOOP   CLEAR    X
        CLEAR    A
        CLEAR    S
        +LDT     #4096
        TD       =X'F1'
        JEQ      *-3
        RD       =X'F1'
        COMPR    A,S
        JEQ      *+11
        STCH     BUFFER,X
        TIXR     T
        JLT      *-19
        STX      LENGTH
        LDA      LENGTH
        COMP     #0
        JEQ      ENDFIL
.WRBUFF   05,BUFFER,LENGTH
        CLEAR    X
        LDT      LENGTH
        LDCH     BUFFER,X
        TD       =X'05'
        JEQ      *-3
        WD       =X'05'
        TIXR     T
        JLT      *-14
        J        CLOOP
.ENDFIL  WRBUFF   05,EOF,THREE
ENDFIL  CLEAR    X
        LDT      THREE
        LDCH     EOF,X
        TD       =X'05'
        JEQ      *-3
        WD       =X'05'
        TIXR     T
        JLT      *-14
        J        @RETADR
EOF     BYTE     C'EOF'
THREE   WORD     3
RETADR  RESW     1
LENGTH  RESW     1
BUFFER  RESB     4096
        END      FIRST
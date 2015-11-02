#ifndef DOS
  #ifndef SPARC
    #ifndef LINUX
      #define DOS 1
    #endif
  #endif
#endif
#include <ctype.h>
#include <memory.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#define BUF_SIZE 121
#define MACSIZE 4096
#define P_TABLE_SIZE 5
#define E_TABLE_SIZE 5
#define R_TABLE_SIZE 5
#define FILE_BUF_SIZE 12000
 
 typedef enum { FALSE = 0, TRUE } BOOLEAN;
 
  struct PTYPE {
    short address;
    char *symptr;
  };
 
 struct ETYPE {
    short address;
    char *symptr;
 };
 
 struct RTYPE {
    short address;
    short module_address;
 };
 
 struct PTYPE P_table[P_TABLE_SIZE];
 struct ETYPE E_table[E_TABLE_SIZE];
 struct RTYPE R_table[R_TABLE_SIZE];
 
 BOOLEAN gots;
 
 char buf[BUF_SIZE], ifilename[BUF_SIZE], ofilename[BUF_SIZE], 
      saves, file_buffer[FILE_BUF_SIZE]; 
 
 short int P_tablex, R_tablex, E_tablex, ssize, filesize,  
           textsize, E_tablexstart, R_tablexstart, ofopen, 
           text_buffer[MACSIZE+1], startadd, module_address;
 
 #ifdef SPARC
           char fdiv = '/';
 #endif
 #ifdef LINUX
           char fdiv = '/';
 #endif
 #ifdef DOS
           char fdiv = '\\';
 #endif
 
 FILE * out_stream;
 FILE * in_stream;
 
 char author[] = "linv1 written by . . .\n";
 
 //==============================================================
 void ierror(void) {
    printf("ERROR: Input file %s is not linkable\n", ifilename);
    exit(1);
 }
 
 //==============================================================
 void processfile(void)
 {
    char firstchar, *fptr, *endptr;
    short i, address;
 
    endptr = file_buffer + filesize;
    fptr = file_buffer;
    for (;;) { 
       firstchar = *fptr++;
       if (firstchar == 'T') {
          textsize = endptr - fptr;
          if (textsize/2 > MACSIZE - module_address) {
              printf("ERROR: Linked program too big\n");
              exit(1);
          }
          // move text into text buffer
           memcpy(&text_buffer[module_address], fptr, textsize);
 
          // add number of words to module_address
          module_address += textsize/2;
          break;
       }
       if (firstchar != 'S' && firstchar != 's' &&
           firstchar != 'P' && firstchar != 'E' && firstchar != 
           'R') 
          ierror();
       else {  // got header entry
          memcpy(&address, fptr, 2);
          fptr = fptr + 2;
          if (fptr > endptr) ierror();
 
          if (firstchar == 'S' || firstchar == 's') {
             if (gots) {
                 printf("ERROR: More than one starting add\n");
                 exit(1);
             }
             gots = TRUE;
             saves = firstchar;
             if (firstchar == 'S')
                startadd = address;
             else
                startadd = address + module_address;
             continue;
          }
 
          if (firstchar == 'P') {
             if (P_tablex >= P_TABLE_SIZE) {
                  printf("ERROR: P table overflow\n");
                  exit(1);
             }
             P_table[P_tablex].address = module_address +
             address;
          }
          else
          if (firstchar == 'E') {
             if (E_tablex >= E_TABLE_SIZE) {
                  printf("ERROR: E table overflow\n");
                  exit(1);
             }
             E_table[E_tablex].address = module_address +
             address;
          }
          else
          if (firstchar == 'R') {
             if (R_tablex >= R_TABLE_SIZE) {
                  printf("ERROR: R table overflow\n");
                  exit(1);
             }
             R_table[R_tablex].module_address = module_address;
             R_table[R_tablex++].address = module_address +
             address;
             continue;
          }
          ssize = strlen(fptr) + 1;
          if (firstchar == 'P') {
             for (i = 0; i < P_tablex; i++)
             if (!strcmp(fptr, P_table[i].symptr)) {
                printf("ERROR: Duplicate PUBLIC symbol %s\n", 
                fptr); 
                exit(1);
             }
             P_table[P_tablex++].symptr = strdup(fptr);
          }
          else
             E_table[E_tablex++].symptr = strdup(fptr); 
          fptr = fptr + strlen(fptr) + 1;
          continue;
 
       }  /* end of header entry processing */
 
    } 
 
    return;
 }
 
 //==============================================================
 // process each input file
 void doifile(void)
 {
    char *pcat;
 
    // does the input file name have an extension?
    if ((pcat=strrchr(ifilename,'.'))== NULL || (pcat &&  
         strchr(pcat,fdiv)))
       strcat(ifilename,".mob"); // add ".mob" to input file name
 #ifdef SPARC
    in_stream = fopen(ifilename, "r");
 #endif
 #ifdef LINUX
    in_stream = fopen(ifilename, "r");
 #endif
 #ifdef DOS
    in_stream = fopen(ifilename, "rb");
 #endif
 
    if (!in_stream) {
       printf("ERROR: Cannot open input file %s\n", ifilename);
       exit(1);
    }
 
    if (!ofopen) {
       ofopen = 1;
       strcpy (ofilename, ifilename);
       // form output file name from first input file name
       strcpy (strrchr(ofilename,'.'),".mac"); 
 
 #ifdef SPARC
       out_stream = fopen(ofilename,"w");
 #endif
 #ifdef LINUX
       out_stream = fopen(ofilename,"w");
 #endif
 #ifdef DOS
       out_stream = fopen(ofilename, "wb");
 #endif
 
        if (!out_stream) {
           printf("ERROR: Cannot open output file %s\n",
                   ofilename);
           exit(1);
        }
    }
 
    filesize = fread(file_buffer, 1, FILE_BUF_SIZE, in_stream);
    fclose(in_stream);
    if (filesize == FILE_BUF_SIZE) {
       printf("Input file %s too big\n", ifilename);
       exit(1);
    }
    processfile();
 }
 
 //==============================================================
 int main(int argc,char *argv[])
 {
     short argx, i, j;
 
     printf("%s", author);
 
     if (argc < 2) {
        printf("ERROR: Incorrect number of command line args\n");
        exit(1);
     }
 
     for (argx = 1; argx < argc; argx++) {
        strcpy(ifilename, argv[argx]);
        doifile();
     }    /* end of arg processing */
 
     // resolve external references
     for (; E_tablexstart < E_tablex; E_tablexstart++) {
        j = 0;
 
     // search for matching public
     while (j < P_tablex && 
            strcmp(P_table[j].symptr,
            E_table[E_tablexstart].symptr))
        j++;
 
        // found it--now resolve external ref
        if (j < P_tablex) {
           text_buffer[E_table[E_tablexstart].address] =
           text_buffer[E_table[E_tablexstart].address] & 0xf000
                               |
           (text_buffer[E_table[E_tablexstart].address] +
                		P_table[j].address ) & 0x0fff;
 
        }
        else
           break;
     }  
 
     if (E_tablexstart !=E_tablex) {   // no more ext references
         printf("ERROR: Unresolved external symbol %s\n",
              E_table[E_tablexstart].symptr);
           exit(1);
     }
 
     // relocate relocatable symbols
     for (; R_tablexstart < R_tablex; R_tablexstart ++ ) {
 
         text_buffer[R_table[R_tablexstart].address] = 
 
         text_buffer[R_table[R_tablexstart].address] & 0xf000
                   |
         (text_buffer[R_table[R_tablexstart].address]
                   +
          R_table[R_tablexstart].module_address) & 0x0fff;
     }
 
     // output header
     for (i = 0; i < P_tablex; i++) {
        fwrite("P" ,1, 1, out_stream);
        fwrite((char *)&P_table[i].address, 2, 1, out_stream);
        ssize = strlen( P_table[i].symptr) + 1;
        fwrite(P_table[i].symptr, 1, ssize, out_stream);
     }   /* end of public output */
 
     for (i = 0; i < R_tablex; i++) {
        fwrite("R", 1, 1, out_stream);
        fwrite((char *)&R_table[i].address, 2, 1, out_stream);
     }
     for (i = 0; i < E_tablex; i++) {
        fwrite("R", 1, 1, out_stream);
     	  fwrite((char *)&E_table[i].address, 2, 1, out_stream);
     }
     if (gots) {
     	   fwrite(&saves, 1, 1, out_stream);
     	   fwrite((char *)&startadd, 2, 1, out_stream);
     }
     fwrite("T", 1, 1, out_stream);
 
     // output text
     fwrite((char *)text_buffer, 2 * module_address, 1,
        out_stream);
 
     fclose(out_stream);
     return 0;
 }
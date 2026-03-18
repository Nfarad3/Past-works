#include <stdio.h>
#include <string.h>
#include <stdlib.h> 
#include <sys/stat.h>
#include <stdbool.h>
#include <errno.h>
#include <ctype.h>
#include <unistd.h>


struct GradeEntry{
  char studentId[11]; //10 digit ID withspace for \0
  char assignmentName[21]; //max 20 char name with space for \0
  unsigned short grade; //use format specifer %hu to print
};
typedef struct GradeEntry Entry; 

struct Node{
  Entry entry;
  struct Node *next;
};


bool file_exists (char *filename) {
  struct stat buffer;
  return (stat (filename, &buffer) == 0);
}

struct Node *newNode(){
  struct Node *newn = malloc(sizeof(struct Node));
  return newn;
}

void toEnd(struct Node *new, struct Node *front) {
  struct Node *temp = front->next, *lastnode = front;
  while(temp) {
    lastnode = temp; 
    temp = temp->next;
  }
  lastnode->next = new;
  return;
}

void freeList(struct Node* first) {
  struct Node* tmp;
  while (first) {
    tmp = first;
    first = first->next;
    free(tmp);
  }
  return;
}

void printing(struct Node *first){
  struct Node *temp = first->next;
  printf("Student ID | Assignment Name      | Grade\n");
  printf("--------------------------------------------\n");
  while(temp){
    printf("%s | %-20s | %hu\n", temp->entry.studentId, temp->entry.assignmentName, temp->entry.grade);
    temp = temp->next;
  }

}

int adding(struct Node *first, char *s) {
  int leng = strlen(s);
  if (leng==10) return 1;
  struct Node *new = newNode();
  strcpy(new->entry.studentId, strtok(s, ":"));
  if (strlen(new->entry.studentId)!=10) {
    free(new);
    return 1;
  }
  strcpy(new->entry.assignmentName, strtok(NULL, ":"));
  if (leng == strlen(new->entry.studentId) + strlen(new->entry.assignmentName)+1) {
    free(new);
    return 1;
  }
  char mhlehh[4];
  strcpy(mhlehh, strtok(NULL, ":"));
  short unsigned greed;
  greed = strtoul(mhlehh, NULL, 10);
  if (greed>100) {
    free(new);
    return 1;
  }
  new->entry.grade = greed;
  new->next=NULL;
  struct Node *temp = first->next;
  while (temp) {
    if(strcmp(temp->entry.studentId, new->entry.studentId)==0 && strcmp(temp->entry.assignmentName, new->entry.assignmentName)==0) {
      return 1;
    }
    temp = temp->next;
  }
  toEnd(new, first);
  return 0;
}

int removing(struct Node *first, char *s) {
  int leng = strlen(s);
  if (leng==10) return 1;
  char idnum[11], assign[21];
  strcpy(idnum, strtok(s, ":"));
  if (strlen(idnum)!=10) return 1;
  strcpy(assign, strtok(NULL, ":"));

  struct Node *temp = first->next, *prev=first; 
  while (temp) {
    if(strcmp(temp->entry.studentId, idnum)==0 && strcmp(temp->entry.assignmentName, assign)==0) {
      prev->next=temp->next;
      free(temp); 
      return 0;
    }
    prev=temp;
    temp = temp->next;
  }
  return 1;
}

int statting(struct Node *first, char *s) {
  int max=0, min=100, sum=0, found=0; 
  struct Node *temp = first->next;
  while (temp) {
    if (strcmp(s, temp->entry.assignmentName)==0) {
      if (temp->entry.grade > max) max = temp->entry.grade; 
      if (temp->entry.grade < min) min = temp->entry.grade;
      sum += temp->entry.grade; 
      found += 1;
    }
    temp = temp->next; 
  }
  if (found) {
    float ave = sum/found;
    printf("Min: %d\n", min);
    printf("Max: %d\n", max);
    printf("Ave: %.2f\n", ave);
    return 0;
  }
  return 1;
}


FILE *open(char *filename) {
  FILE *file = fopen(filename, "r");
  if (file == NULL) {
    int error = errno;
    if (error == ENOENT) {
      fprintf(stderr, "File '%s' does not exist\n", filename);
    }
    else if (error == EACCES) {
      fprintf(stderr, "Permission denied for file '%s'\n", filename);
    } else {
      fprintf(stderr, "Something went wrong when opening file '%s'\n", filename);
    }
    exit(1);
    }
  return file;
}

int main(int argc, char **argv) {
  if (argc != 2) { 
    fprintf(stderr, "Incorrect number of arguments provided.");
    return 1;
  }
  if (!file_exists(argv[1])) {
    fprintf(stderr, "No such file exists");
    return 1;
  }

  FILE *input;
  char *filename = argv[1];
  input = open(filename);

  struct Node *first, *new;
  first = malloc(sizeof(struct Node));
  first->next=NULL;

  char *s = NULL;
  size_t nbytes = 0;
  ssize_t nchars;
  while (1) {
    nchars = getline(&s, &nbytes, input);
    if (nchars ==-1) break; // EOF
    if (s == NULL) exit(1); // OOM
    s[nchars- 1] = '\0'; // clear newline
    nchars--; // removed newline char
    // inputted string stored in s
    
    new = newNode();
    strcpy(new->entry.studentId, strtok(s, ":"));
    strcpy(new->entry.assignmentName, strtok(NULL, ":"));
    char mhlehh[4];
    strcpy(mhlehh, strtok(NULL, ":"));
    short unsigned greed;
    greed = strtoul(mhlehh, NULL, 10);
    new->entry.grade = greed;
    new->next=NULL;
    toEnd(new, first);
  }

  while (1) {
    nchars = getline(&s, &nbytes, stdin);
    if (nchars ==-1) break; // EOF
    if (s == NULL) exit(1); // OOM
    s[nchars- 1] = '\0'; // clear newline
    nchars--; // removed newline char
    // inputted string stored in s

    if (strncmp(s, "print", 5)==0) printing(first);
    
    if (strncmp(s, "add ", 4)==0) {
      if (strlen(s) <5) continue; 
      int check = adding(first, s+4);
      if (check) fprintf(stderr, "Error adding to list\n");
    }
    
    if (strncmp(s, "remove ", 7) == 0) {
      if (strlen(s) <8) continue;
      int check = removing(first, s+7);
      if (check) fprintf(stderr, "Error removing from list\n");
    }
    
    if (strncmp(s, "stats ", 6) == 0) {
      if (strlen(s) <7) continue; 
      int check = statting(first, s+6);
      if (check) fprintf(stderr, "Error statting from list\n");

    }
  }

  fclose(input);


  char template[] = "./XXXXXX"; 
  int fd = mkstemp(template);
  FILE *tempor = fopen(template, "r+");

  struct Node *temp = first->next; 
  while (temp) {
    fprintf(tempor, "%s:%s:%hu\n", temp->entry.studentId, temp->entry.assignmentName, temp->entry.grade);
    temp = temp->next;
  }
  
  FILE *database; 
  database = fopen(filename, "w");
  rewind(tempor);
 
  int character;
  while ((character = fgetc(tempor)) != EOF) {
    fputc(character, database);
  }

  fclose(database);
  fclose(tempor); 
  unlink(template);
  freeList(first);
  free(s);
  return 0;
}









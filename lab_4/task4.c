char password[8] = "secret";
int main() {
    char input[8];
    int x;
    printf("please enter your password\n");
    scanf("%s", input);
    for(x=0; x<=7; x++) {
        if ((input[x]) > 64 && (input[x]) <= 90) {
            input[x] = input[x] + 32;
        }
    }    
        
    if(strcmp(input, password)==0) {
        return 0;
    } else {
        return -1;
    }
}
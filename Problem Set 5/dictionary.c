// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdio.h>
#include <strings.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

//Declare Variables
unsigned int word_count;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //Hash the word to obtain a hash value
    hash_value = hash(word);

    //Point cursor to the first node
    node *cursor = table[hash_value];

    //Go through the linked list
    while (cursor != 0)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned long total = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open dictionary
    FILE *file = fopen(dictionary, "r");

    //Return NULL if file cannot be opened
    if (file == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }
    // Declare variable called word
    char word[LENGTH + 1];

    //
    while (fscanf(file, "%s", word) != EOF)
    {
        //Allocate memory for each new node
        node *n = malloc(sizeof(node));

        //If malloc returns NULL, return false
        if (n == NULL)
        {
            return false;
        }
        //Copy Word into Node
        strcpy(n -> word, word);
        hash_value = hash(word);
        n -> next = table[hash_value];
        table[hash_value] = n;
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        //If cursor is not NULL, free memory
        while (cursor != NULL)
        {
            //Create temp
            node *tmp = cursor;
            //Move cursor to next node
            cursor = cursor->next;
            //Free up temp
            free(tmp);
        }
        //If cursor is NULL
        if (cursor == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}

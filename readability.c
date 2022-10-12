#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
int count_letters(string text);
int count_words(string text);
int count_scentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    int count_letters(string text);
    int count_words(string text);
    int count_scentences(string text);

    //Compute and return number for text
    int letters = 0;

    //Add 1 for every alphabetical character
    int length = strlen(text);
    for (int i = 0; i < length; i++)
    {
        if
        (isalpha(text[i]))
        {
            letters++;
        }
    }
    //Compute and return number for text
    int words = 1;
    for (int i = 1; i < length; i++)
    {
        if
        (text[i] == ' ')
        {
            words++;
        }
    }
    //Compute and return number for text
    int scentences = 0;
    for (int i = 0; i < length; i++)
    {
        if
        (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            scentences++;
        }
    }
    //equation for grading.
    float calculation = ((0.0588 * letters / words * 100) - (0.296 * scentences / words * 100) - 15.8);
    int index = round(calculation);
    //conditions for final print statement
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
    //good practice to return zero despite not neccesary
    return 0;
}




